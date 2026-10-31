import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from PySide6.QtCore import QThread, Signal

from core.pipeline import ImagePipeline
from export.naming import NamingEngine
from history.manager import HistoryManager


def _init_worker_process():
    """Initializer for child worker processes.

    Registers Pillow plugins like HEIF / AVIF inside each worker process so they
    are immediately available for all format operations.
    """
    try:
        import pillow_heif

        pillow_heif.register_heif_opener()
    except Exception:
        pass

    try:
        import pillow_avif  # noqa: F401
    except Exception:
        pass


def _process_image_task(task):
    """Isolated worker function executed inside process pool child processes.

    Parameters
    ----------
    task : dict
        Contains 'index', 'source', 'output_path', and 'config'.

    Returns
    -------
    dict
        Result dictionary containing execution details, status, and error message.
    """
    index = task["index"]
    source = Path(task["source"])
    output_path = Path(task["output_path"])
    config = task["config"]

    output_settings = config.get("output", {})
    format_name = output_settings.get("format")
    operations = config.get("operations", [])

    try:
        if not source.exists():
            raise FileNotFoundError(f"File not found: {source}")

        pipeline = ImagePipeline()
        # record_history=False: history is batch-recorded safely in the main process
        result = pipeline.run(source, output_path, config, record_history=False)

        return {
            "index": index,
            "source": str(source),
            "output": str(result),
            "status": "success",
            "format": format_name,
            "operations": operations,
            "error": None,
        }

    except Exception as error:
        return {
            "index": index,
            "source": str(source),
            "output": str(output_path),
            "status": "failed",
            "format": format_name,
            "operations": operations,
            "error": str(error),
        }


class BatchWorker:
    def __init__(self, max_workers=None):
        self.naming = NamingEngine()
        self.history = HistoryManager()
        self.max_workers = max_workers

    def get_worker_count(self, file_count, config=None):
        """Calculate optimal worker count for multi-core parallelism."""
        config = config or {}
        requested = config.get("workers", self.max_workers)
        if requested is not None and int(requested) > 0:
            return max(1, min(int(requested), file_count))

        cpu_count = os.cpu_count() or 4
        # Fully utilize all logical CPU cores, bounded by the number of files
        return max(1, min(cpu_count, file_count))

    def run(
        self, files, output_folder, config, progress_callback=None, cancel_check=None
    ):
        if not files:
            raise ValueError("No files to process")

        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)

        total = len(files)
        results = {
            "success": [],
            "failed": [],
            "cancelled": False,
            "total": total,
            "processed": 0,
        }

        # Fast scan of existing filenames in output folder (single directory pass)
        existing_filenames = set()
        if output_folder.is_dir():
            try:
                with os.scandir(output_folder) as scanner:
                    existing_filenames = {
                        os.path.normcase(entry.name)
                        for entry in scanner
                        if entry.is_file()
                    }
            except OSError:
                pass

        # Pre-allocate collision-free output paths in memory (< 15ms for 2000 files)
        reserved_paths = set()
        tasks = []
        for index, file_item in enumerate(files):
            source = Path(file_item)
            task_config = dict(config)
            output_settings = dict(config.get("output", {}))

            target_path = self.naming.generate(
                source,
                output_folder,
                output_settings,
                reserved_paths=reserved_paths,
                existing_filenames=existing_filenames,
            )

            task_config["output"] = dict(output_settings)
            task_config["output"]["target_path"] = str(target_path)

            tasks.append({
                "index": index,
                "source": str(source),
                "output_path": str(target_path),
                "config": task_config,
            })

        num_workers = self.get_worker_count(total, config)
        force_sequential = config.get("sequential", False)

        # For a single image or when sequential is forced, process in-process
        if total <= 1 or num_workers <= 1 or force_sequential:
            return self._run_sequential(
                tasks, results, progress_callback, cancel_check
            )

        # Multi-Core Parallel Processing via ProcessPoolExecutor
        try:
            return self._run_multiprocessing(
                tasks, num_workers, results, progress_callback, cancel_check
            )
        except (OSError, PermissionError):
            # Fallback for environments where process spawning is restricted
            return self._run_sequential(
                tasks, results, progress_callback, cancel_check
            )

    def _run_sequential(self, tasks, results, progress_callback, cancel_check):
        total = len(tasks)
        history_records = []

        for item in tasks:
            index = item["index"]
            source = Path(item["source"])

            if cancel_check and cancel_check():
                results["cancelled"] = True
                if progress_callback:
                    progress_callback(index, total, source.name, "Cancelled")
                break

            if progress_callback:
                progress_callback(index, total, source.name, "Processing")

            task_result = _process_image_task(item)
            history_records.append(task_result)

            if task_result["status"] == "success":
                results["success"].append(task_result["output"])
                status = "Completed"
            else:
                results["failed"].append({
                    "file": task_result["source"],
                    "error": task_result["error"],
                })
                status = "Failed"

            results["processed"] = index + 1
            if progress_callback:
                progress_callback(index + 1, total, source.name, status)

        if history_records:
            try:
                self.history.add_batch(history_records)
            except Exception:
                pass

        return results

    def _run_multiprocessing(
        self, tasks, num_workers, results, progress_callback, cancel_check
    ):
        total = len(tasks)
        history_records = []
        results_by_index = {}
        processed_count = 0

        executor = ProcessPoolExecutor(
            max_workers=num_workers,
            initializer=_init_worker_process,
        )

        try:
            future_to_task = {
                executor.submit(_process_image_task, task): task for task in tasks
            }

            for future in as_completed(future_to_task):
                task = future_to_task[future]
                source_name = Path(task["source"]).name

                # Immediate cancellation check
                if cancel_check and cancel_check():
                    results["cancelled"] = True
                    for fut in future_to_task:
                        fut.cancel()

                    try:
                        for proc in getattr(executor, "_processes", {}).values():
                            if proc and proc.is_alive():
                                proc.terminate()
                    except Exception:
                        pass

                    executor.shutdown(wait=False, cancel_futures=True)

                    if progress_callback:
                        progress_callback(
                            processed_count, total, source_name, "Cancelled"
                        )
                    break

                try:
                    task_result = future.result()
                except Exception as exc:
                    task_result = {
                        "index": task["index"],
                        "source": task["source"],
                        "output": task["output_path"],
                        "status": "failed",
                        "format": task["config"].get("output", {}).get("format"),
                        "operations": task["config"].get("operations", []),
                        "error": str(exc),
                    }

                processed_count += 1
                results_by_index[task_result["index"]] = task_result
                history_records.append(task_result)

                status = (
                    "Completed" if task_result["status"] == "success" else "Failed"
                )
                if progress_callback:
                    progress_callback(processed_count, total, source_name, status)

        except Exception:
            # Handle abrupt pool termination during cancellation or unexpected issues
            pass
        finally:
            if results["cancelled"]:
                executor.shutdown(wait=False, cancel_futures=True)
            else:
                executor.shutdown(wait=True)

        # Assemble results in deterministic order matching the original file list
        for idx in sorted(results_by_index.keys()):
            item = results_by_index[idx]
            if item["status"] == "success":
                results["success"].append(item["output"])
            else:
                results["failed"].append({
                    "file": item["source"],
                    "error": item["error"],
                })

        results["processed"] = processed_count

        # Batch record history safely in the main process
        if history_records:
            try:
                self.history.add_batch(history_records)
            except Exception:
                pass

        return results

    def create_output_path(self, source, output_folder, config):
        output_settings = config.get("output", {})
        if not output_settings:
            raise ValueError("Output configuration missing")

        format_name = output_settings.get("format")

        if output_settings.get("keep_format"):
            extension = source.suffix.replace(".", "")
        else:
            if not format_name:
                raise ValueError("Output format missing")
            extension = self.naming.normalize_extension(format_name)

        filename = source.stem + "_processed" + "." + extension
        return Path(output_folder) / filename


class WorkerThread(QThread):
    progress_changed = Signal(int, int, str, str)
    processing_finished = Signal(dict)
    processing_error = Signal(str)

    def __init__(self, files, output_folder, config, max_workers=None):
        super().__init__()
        self.files = files
        self.output_folder = output_folder
        self.config = config
        self.worker = BatchWorker(max_workers=max_workers)
        self._cancelled = False

    def run(self):
        self._cancelled = False
        try:
            result = self.worker.run(
                self.files,
                self.output_folder,
                self.config,
                progress_callback=self.emit_progress,
                cancel_check=self.is_cancelled,
            )
            self.processing_finished.emit(result)
        except Exception as error:
            self.processing_error.emit(str(error))

    def emit_progress(self, current, total, filename, status):
        self.progress_changed.emit(current, total, filename, status)

    def cancel(self):
        self._cancelled = True

    def is_cancelled(self):
        return self._cancelled

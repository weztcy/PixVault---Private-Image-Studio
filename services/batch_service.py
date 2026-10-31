import os
from PySide6.QtCore import QObject, Signal

from core.worker import WorkerThread


class BatchService(QObject):
    progress_changed = Signal(int, int, str, str)

    processing_finished = Signal(dict)

    processing_error = Signal(str)

    processing_cancelled = Signal()

    def __init__(self, max_workers=None):

        super().__init__()

        self.thread = None
        self.max_workers = max_workers

    @staticmethod
    def get_cpu_cores():
        """Return the number of logical CPU cores available on this system."""
        return os.cpu_count() or 4

    def get_max_workers(self):
        """Return configured max workers, or detected CPU cores if not set."""
        if self.max_workers is not None and self.max_workers > 0:
            return self.max_workers
        return self.get_cpu_cores()

    def set_max_workers(self, workers):
        """Configure max worker processes for parallel processing."""
        self.max_workers = int(workers) if workers is not None else None

    def start_batch(self, files, output_folder, config, max_workers=None):

        if self.is_running():
            raise RuntimeError("Batch processing is already running")

        if not files:
            raise ValueError("No files provided")

        if not output_folder:
            raise ValueError("Output folder is required")

        if not config:
            raise ValueError("Processing configuration missing")

        workers = max_workers if max_workers is not None else self.max_workers

        self.thread = WorkerThread(
            files, output_folder, config, max_workers=workers
        )

        self.connect_thread()

        self.thread.start()

    def connect_thread(self):

        if not self.thread:
            return

        self.thread.progress_changed.connect(self.progress_changed.emit)

        self.thread.processing_finished.connect(self.on_finished)

        self.thread.processing_error.connect(self.on_error)

        self.thread.finished.connect(self.cleanup_thread)

    def cancel(self):

        if not self.thread:
            return

        if self.thread.isRunning():
            self.thread.cancel()

            self.processing_cancelled.emit()

    def on_finished(self, result):

        self.processing_finished.emit(result)

    def on_error(self, error):

        self.processing_error.emit(error)

    def is_running(self):

        if not self.thread:
            return False

        return self.thread.isRunning()

    def cleanup_thread(self):

        if not self.thread:
            return

        self.thread.deleteLater()

        self.thread = None

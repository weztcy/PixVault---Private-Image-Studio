"""Stylesheet module for UI components.

Visual rules were extracted from the component files so the UI modules stay focused on behavior.
"""

EXPORT_PROGRESS_QSS = """
            /* MAIN WIDGET */

            QWidget#export_progress_widget {
                background: transparent;
                border: none;
            }

            /* MAIN CARD */

            QFrame#export_progress_card {
                background-color: #141e30;
                border: 1px solid #29374c;
                border-radius: 16px;
            }

            /* EYEBROW */

            QLabel#export_eyebrow {
                color: #5eead4;
                background: transparent;
                border: none;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            /* TITLE */

            QLabel#export_title {
                color: #f1f5f9;
                background: transparent;
                border: none;
                font-family: "Segoe UI";
                font-size: 19px;
                font-weight: 700;
            }

            /* DESCRIPTION */

            QLabel#export_description {
                color: #94a3b8;
                background: transparent;
                border: none;
                font-family: "Segoe UI";
                font-size: 12px;
            }

            /* STATUS BADGE */

            QFrame#export_status_badge {
                border-radius: 9px;
                padding: 0;
            }

            QFrame#export_status_badge[
                process_state="ready"
            ] {
                background-color: #263449;
                border: 1px solid #394a61;
            }

            QFrame#export_status_badge[
                process_state="processing"
            ] {
                background-color: #173a40;
                border: 1px solid #28665f;
            }

            QFrame#export_status_badge[
                process_state="completed"
            ] {
                background-color: #173e43;
                border: 1px solid #28665f;
            }

            QFrame#export_status_badge[
                process_state="failed"
            ] {
                background-color: #44252e;
                border: 1px solid #75404c;
            }

            QFrame#export_status_badge[
                process_state="cancelled"
            ] {
                background-color: #443820;
                border: 1px solid #77602a;
            }

            /* STATUS TEXT */

            QLabel#export_status_text,
            QLabel#export_status_indicator {
                background: transparent;
                border: none;
                font-family: "Segoe UI";
                font-size: 11px;
                font-weight: 700;
            }

            QLabel#export_status_text[
                process_state="ready"
            ],
            QLabel#export_status_indicator[
                process_state="ready"
            ] {
                color: #94a3b8;
            }

            QLabel#export_status_text[
                process_state="processing"
            ],
            QLabel#export_status_indicator[
                process_state="processing"
            ],
            QLabel#export_status_text[
                process_state="completed"
            ],
            QLabel#export_status_indicator[
                process_state="completed"
            ] {
                color: #5eead4;
            }

            QLabel#export_status_text[
                process_state="failed"
            ],
            QLabel#export_status_indicator[
                process_state="failed"
            ] {
                color: #fca5a5;
            }

            QLabel#export_status_text[
                process_state="cancelled"
            ],
            QLabel#export_status_indicator[
                process_state="cancelled"
            ] {
                color: #fcd34d;
            }

            /* PROGRESS HEADER */

            QLabel#export_section_label {
                color: #94a3b8;
                background: transparent;
                border: none;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            /* PERCENTAGE */

            QLabel#export_percentage {
                color: #5eead4;
                background: transparent;
                border: none;
                font-family: "Segoe UI";
                font-size: 16px;
                font-weight: 800;
            }

            /* PROGRESS BAR */

            QProgressBar#export_progress_bar {
                background-color: #26384d;
                border: none;
                border-radius: 6px;
                text-align: center;
            }

            QProgressBar#export_progress_bar::chunk {
                background-color: #5eead4;
                border-radius: 6px;
            }

            QProgressBar#export_progress_bar[
                process_state="failed"
            ]::chunk {
                background-color: #f87171;
            }

            QProgressBar#export_progress_bar[
                process_state="cancelled"
            ]::chunk {
                background-color: #fbbf24;
            }

            /* INFORMATION CARDS */

            QFrame#export_info_card {
                background-color: #1b2940;
                border: 1px solid #304259;
                border-radius: 10px;
            }

            /* INFO TITLES */

            QLabel#export_info_title {
                color: #64748b;
                background: transparent;
                border: none;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            /* FILE NAME */

            QLabel#export_file_label {
                color: #d5deea;
                background: transparent;
                border: none;
                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 500;
            }

            /* FILE COUNTER */

            QLabel#export_counter_label {
                color: #f1f5f9;
                background: transparent;
                border: none;
                font-family: "Segoe UI";
                font-size: 17px;
                font-weight: 700;
            }

            /* FOOTER TEXT */

            QLabel#export_footer_text {
                color: #64748b;
                background: transparent;
                border: none;
                font-family: "Segoe UI";
                font-size: 11px;
            }

            /* OPEN FOLDER BUTTON */

            QPushButton#export_open_button {
                background-color: #173a40;
                color: #5eead4;
                border: 1px solid #28665f;
                border-radius: 9px;
                padding: 8px 16px;
                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 700;
            }

            QPushButton#export_open_button:hover {
                background-color: #1c4649;
                color: #99f6e4;
                border: 1px solid #5eead4;
            }

            QPushButton#export_open_button:pressed {
                background-color: #285d60;
            }

            QPushButton#export_open_button:focus {
                border: 1px solid #99f6e4;
            }

            QPushButton#export_open_button:disabled {
                background-color: #202b3b;
                color: #64748b;
                border: 1px solid #354459;
            }
            """


def apply_export_progress_style(widget):
    """Apply the EXPORT_PROGRESS_QSS stylesheet to *widget*."""
    widget.setStyleSheet(EXPORT_PROGRESS_QSS)

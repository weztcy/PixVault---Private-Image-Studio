"""Stylesheet module for UI components.

Visual rules were extracted from the component files so the UI modules stay focused on behavior.
"""

OUTPUT_SELECTOR_QSS = """
            /* MAIN COMPONENT */

            QWidget#output_selector {
                background: transparent;
                border: none;
            }

            /* MAIN CARD */

            QFrame#output_selector_card {
                background-color: #141e30;
                border: 1px solid #29374c;
                border-radius: 16px;
            }

            /* HEADER EYEBROW */

            QLabel#output_eyebrow {
                color: #5eead4;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            /* HEADER TITLE */

            QLabel#output_title {
                color: #f1f5f9;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 19px;
                font-weight: 700;
            }

            /* HEADER DESCRIPTION */

            QLabel#output_description {
                color: #94a3b8;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 12px;
            }

            /* LOCAL STORAGE BADGE */

            QLabel#output_local_badge {
                background-color: #173a40;
                color: #5eead4;

                border: 1px solid #28665f;
                border-radius: 8px;

                padding: 7px 11px;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            /* SECTION LABELS */

            QLabel#output_section_label {
                color: #94a3b8;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            /* RADIO MODE CARDS */

            QRadioButton#output_mode_radio {
                background-color: #1b2940;
                color: #d5deea;

                border: 1px solid #304259;
                border-radius: 10px;

                padding: 11px 15px;
                spacing: 12px;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 600;
            }

            QRadioButton#output_mode_radio:hover {
                background-color: #203149;
                color: #f8fafc;

                border: 1px solid #426273;
            }

            QRadioButton#output_mode_radio:checked {
                background-color: #173a40;
                color: #5eead4;

                border: 1px solid #397d76;
                border-left: 3px solid #5eead4;

                font-weight: 700;
            }

            QRadioButton#output_mode_radio:checked:hover {
                background-color: #1c4649;
                color: #99f6e4;

                border: 1px solid #5eead4;
                border-left: 3px solid #5eead4;
            }

            /* RADIO INDICATOR */

            QRadioButton#output_mode_radio::indicator {
                width: 18px;
                height: 18px;

                background-color: #101b2d;

                border: 2px solid #50647c;
                border-radius: 11px;
            }

            QRadioButton#output_mode_radio::indicator:hover {
                border: 2px solid #5eead4;
            }

            QRadioButton#output_mode_radio::indicator:checked {
                background-color: #5eead4;

                border: 5px solid #173a40;
                border-radius: 11px;
            }

            QRadioButton#output_mode_radio:focus {
                border-color: #5eead4;
            }

            /* FOLDER PATH SECTION */

            QFrame#output_path_section {
                background-color: #19283c;

                border: 1px solid #304259;
                border-radius: 11px;
            }

            /* MODE BADGES */

            QLabel#output_mode_badge {
                border-radius: 7px;

                padding: 5px 10px;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
            }

            QLabel#output_mode_badge[mode="default"] {
                background-color: #263449;
                color: #cbd5e1;
                border: 1px solid #394a61;
            }

            QLabel#output_mode_badge[mode="custom"] {
                background-color: #173e43;
                color: #5eead4;
                border: 1px solid #28665f;
            }

            QLabel#output_mode_badge[mode="fallback"] {
                background-color: #443820;
                color: #fcd34d;
                border: 1px solid #77602a;
            }

            /* FOLDER PATH INPUT */

            QLineEdit#output_folder_input {
                background-color: #101b2d;

                color: #d5deea;

                border: 1px solid #304259;
                border-radius: 9px;

                padding: 10px 13px;

                font-family: "Consolas";
                font-size: 12px;

                selection-background-color: #285d60;
                selection-color: #f8fafc;
            }

            QLineEdit#output_folder_input:hover {
                border: 1px solid #426273;
            }

            QLineEdit#output_folder_input:focus {
                border: 1px solid #5eead4;
            }

            /* COPY PATH BUTTON */

            QPushButton#output_copy_button {
                background-color: #1b2940;
                color: #d5deea;

                border: 1px solid #38536b;
                border-radius: 9px;

                padding: 8px 16px;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton#output_copy_button:hover {
                background-color: #24384e;
                color: #f8fafc;
                border-color: #5eead4;
            }

            QPushButton#output_copy_button:pressed {
                background-color: #285d60;
            }

            /* BROWSE BUTTON */

            QPushButton#output_browse_button {
                background-color: #5eead4;
                color: #0b1120;

                border: 1px solid #5eead4;
                border-radius: 9px;

                padding: 8px 18px;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 700;
            }

            QPushButton#output_browse_button:hover {
                background-color: #99f6e4;
                border-color: #99f6e4;
            }

            QPushButton#output_browse_button:pressed {
                background-color: #2dd4bf;
                border-color: #2dd4bf;
            }

            /* KEYBOARD FOCUS */

            QPushButton#output_copy_button:focus,
            QPushButton#output_browse_button:focus {
                border: 2px solid #99f6e4;
            }

            /* HELPER TEXT */

            QLabel#output_helper_text {
                color: #64748b;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 11px;
            }

            /* DISABLED STATES */

            QRadioButton#output_mode_radio:disabled,
            QPushButton#output_copy_button:disabled,
            QPushButton#output_browse_button:disabled {
                background-color: #202b3b;
                color: #64748b;
                border: 1px solid #354459;
            }

            QLineEdit#output_folder_input:disabled {
                background-color: #151e2d;
                color: #64748b;
                border: 1px solid #253348;
            }
            """


def apply_output_selector_style(widget):
    """Apply the OUTPUT_SELECTOR_QSS stylesheet to *widget*."""
    widget.setStyleSheet(OUTPUT_SELECTOR_QSS)

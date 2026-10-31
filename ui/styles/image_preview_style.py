"""Stylesheet module for UI components.

Visual rules were extracted from the component files so the UI modules stay focused on behavior.
"""

IMAGE_PREVIEW_QSS = """
            /* MAIN WIDGET */

            QWidget#image_preview_widget {
                background: transparent;
                border: none;
            }

            /* MAIN CARD */

            QFrame#image_preview_card {
                background-color: #141e30;
                border: 1px solid #29374c;
                border-radius: 16px;
            }

            /* HEADER ICON */

            QFrame#image_preview_icon_box {
                background-color: #173a40;
                border: 1px solid #285d60;
                border-radius: 11px;
            }

            QLabel#image_preview_header_icon {
                color: #5eead4;
                background: transparent;
                border: none;

                font-family: "Segoe UI Symbol";
                font-size: 25px;
                font-weight: 700;
            }

            /* HEADER TEXT */

            QLabel#image_preview_eyebrow {
                color: #5eead4;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
            }

            QLabel#image_preview_title {
                color: #f1f5f9;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 19px;
                font-weight: 700;
            }

            QLabel#image_preview_subtitle {
                color: #94a3b8;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 11px;
            }

            /* STATUS BADGE */

            QLabel#image_preview_status {
                border-radius: 8px;

                padding: 7px 11px;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
            }

            QLabel#image_preview_status[
                preview_state="empty"
            ] {
                background-color: #263449;
                color: #94a3b8;
                border: 1px solid #394a61;
            }

            QLabel#image_preview_status[
                preview_state="loaded"
            ] {
                background-color: #173e43;
                color: #5eead4;
                border: 1px solid #28665f;
            }

            QLabel#image_preview_status[
                preview_state="error"
            ] {
                background-color: #44252e;
                color: #fca5a5;
                border: 1px solid #75404c;
            }

            /* PREVIEW CANVAS */

            QFrame#image_preview_canvas {
                background: qlineargradient(
                    x1:0, y1:0,
                    x2:1, y2:1,
                    stop:0 #0c1727,
                    stop:1 #101c30
                );

                border: 1px dashed #35526a;
                border-radius: 13px;
            }

            /* STACK CONTENT */

            QStackedWidget#image_preview_stack,
            QWidget#image_preview_empty_page,
            QWidget#image_preview_image_page {
                background: transparent;
                border: none;
            }

            /* IMAGE DISPLAY */

            QLabel#image_preview_display {
                background: transparent;
                border: none;
            }

            /* EMPTY ICON BOX */

            QFrame#image_preview_empty_icon_box {
                background-color: #173a40;
                border: 1px solid #285d60;
                border-radius: 18px;
            }

            QLabel#image_preview_empty_icon {
                color: #5eead4;
                background: transparent;
                border: none;

                font-family: "Segoe UI Symbol";
                font-size: 37px;
            }

            /* EMPTY TITLE */

            QLabel#image_preview_empty_title {
                color: #f1f5f9;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 17px;
                font-weight: 700;
            }

            /* EMPTY DESCRIPTION */

            QLabel#image_preview_empty_description {
                color: #94a3b8;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 12px;
            }

            /* FOOTER */

            QFrame#image_preview_footer {
                background-color: #1b2940;
                border: 1px solid #304259;
                border-radius: 10px;
            }

            QLabel#image_preview_file_icon {
                color: #5eead4;
                background: transparent;
                border: none;

                font-family: "Segoe UI Symbol";
                font-size: 20px;
                font-weight: 700;
            }

            QLabel#image_preview_filename {
                color: #d5deea;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 600;
            }

            QLabel#image_preview_resolution {
                color: #94a3b8;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 11px;
            }

            /* FORMAT BADGE */

            QLabel#image_preview_format {
                background-color: #173a40;
                color: #5eead4;

                border: 1px solid #28665f;
                border-radius: 6px;

                padding: 5px 9px;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
            }
            """


def apply_image_preview_style(widget):
    """Apply the IMAGE_PREVIEW_QSS stylesheet to *widget*."""
    widget.setStyleSheet(IMAGE_PREVIEW_QSS)

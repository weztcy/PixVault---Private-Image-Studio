"""Stylesheet module for UI components.

Visual rules were extracted from the component files so the UI modules stay focused on behavior.
"""

MAIN_WINDOW_QSS = """
            /* =========================
               MAIN WINDOW
            ========================= */

            QMainWindow#pixvault_main_window {
                background-color: #0b1120;
            }

            QWidget#main_container {
                background-color: #0b1120;
            }

            QWidget#main_content {
                background-color: #0b1120;
            }

            QStackedWidget#main_workspace {
                background-color: #0b1120;
                border: none;
            }

            /* =========================
               PREMIUM HEADER
            ========================= */

            QFrame#main_header {
                background-color: #101b2d;

                border: none;
                border-bottom: 1px solid #29374c;
            }

            /* =========================
               BRAND ICON
            ========================= */

            QLabel#main_brand_icon {
                background: transparent;
                border: none;
                padding: 0;
            }

            /* =========================
               BRAND TITLE
            ========================= */

            QLabel#main_brand_title {
                color: #f8fafc;

                background: transparent;
                border: none;
                padding: 0;
                margin: 0;
                margin-bottom: -3px;

                font-family: "Segoe UI";
                font-size: 19px;
                font-weight: 800;

                letter-spacing: 2px;
            }

            /* =========================
               BRAND SUBTITLE
            ========================= */

            QLabel#main_brand_subtitle {
                color: #5eead4;

                background: transparent;
                border: none;
                padding: 0;
                margin: 0;

                font-family: "Segoe UI";
                font-size: 9px;
                font-weight: 700;

                letter-spacing: 1px;
            }

            /* =========================
               HEADER INFO
            ========================= */

            QLabel#main_header_info {
                color: #cbd5e1;

                background: transparent;
                border: none;
                padding: 0;
                margin: 0;
                margin-bottom: -2px;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 600;
            }

            QLabel#main_header_subtitle {
                color: #64748b;

                background: transparent;
                border: none;
                padding: 0;
                margin: 0;

                font-family: "Segoe UI";
                font-size: 10px;
            }

            /* =========================
               LOCAL STATUS CARD
            ========================= */

            QFrame#main_status_card {
                background-color: #142b35;

                border: 1px solid #294d51;
                border-radius: 12px;
            }

            /* =========================
               STATUS INDICATOR
            ========================= */

            QLabel#main_status_indicator {
                color: #5eead4;

                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 13px;
            }

            /* =========================
               STATUS TITLE
            ========================= */

            QLabel#main_status_title {
                color: #5eead4;

                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;

                letter-spacing: 1px;
            }

            /* =========================
               STATUS DESCRIPTION
            ========================= */

            QLabel#main_status_description {
                color: #94a3b8;

                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 10px;
            }
            """


def apply_main_window_style(widget):
    """Apply the MAIN_WINDOW_QSS stylesheet to *widget*."""
    widget.setStyleSheet(MAIN_WINDOW_QSS)

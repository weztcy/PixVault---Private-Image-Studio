"""Stylesheet module for UI components.

Visual rules were extracted from the component files so the UI modules stay focused on behavior.
"""

SIDEBAR_QSS = """
            /* =========================
               SIDEBAR BACKGROUND
            ========================= */

            QWidget#pixvault_sidebar {
                background-color: #0f1728;
                border-right: 1px solid #26364b;
            }

            QWidget#sidebar_nav_container,
            QWidget#sidebar_footer_container {
                background-color: #0f1728;
            }

            QScrollArea#sidebar_scroll {
                background-color: #0f1728;
                border: none;
            }

            /* =========================
               SECTION LABEL
            ========================= */

            QLabel#sidebar_section {
                color: #64748b;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
                background: transparent;
                border: none;
            }

            /* =========================
               NAVIGATION BUTTON
            ========================= */

            QPushButton#sidebar_nav_button {
                background-color: transparent;

                color: #a7b5c9;

                border: 1px solid transparent;
                border-left: 3px solid transparent;

                border-radius: 9px;

                text-align: left;

                padding-left: 14px;
                padding-right: 8px;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 500;
            }

            /* =========================
               HOVER
            ========================= */

            QPushButton#sidebar_nav_button:hover:!checked {
                background-color: #1b2b40;

                color: #f1f5f9;

                border: 1px solid #304259;
                border-left: 3px solid transparent;
            }

            /* =========================
               ACTIVE PAGE
            ========================= */

            QPushButton#sidebar_nav_button:checked {
                background-color: #173a40;

                color: #5eead4;

                border: 1px solid #285d60;
                border-left: 3px solid #5eead4;

                font-weight: 700;
            }

            QPushButton#sidebar_nav_button:checked:hover {
                background-color: #1c4649;
                color: #99f6e4;
            }

            /* =========================
               PRESSED
            ========================= */

            QPushButton#sidebar_nav_button:pressed {
                background-color: #244b52;
            }

            /* =========================
               KEYBOARD FOCUS
            ========================= */

            QPushButton#sidebar_nav_button:focus:!checked {
                border: 1px solid #5eead4;
                border-left: 3px solid #5eead4;
            }

            /* =========================
               FOOTER
            ========================= */

            QFrame#sidebar_footer_card {
                background-color: #142b35;

                border: 1px solid #294d51;

                border-radius: 12px;
            }

            QLabel#sidebar_status_indicator {
                color: #5eead4;

                font-family: "Segoe UI";
                font-size: 10px;

                background: transparent;
                border: none;
            }

            QLabel#sidebar_status_title {
                color: #5eead4;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;

                background: transparent;
                border: none;
            }

            QLabel#sidebar_footer_description {
                color: #94a3b8;

                font-family: "Segoe UI";
                font-size: 10px;

                background: transparent;
                border: none;
            }

            /* =========================
               SCROLLBAR
            ========================= */

            QScrollBar:vertical {
                background: #0f1728;

                width: 5px;

                margin: 0;
                border: none;
            }

            QScrollBar::handle:vertical {
                background: #334155;

                border-radius: 2px;

                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background: #5eead4;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
                border: none;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }
            """


def apply_sidebar_style(widget):
    """Apply the SIDEBAR_QSS stylesheet to *widget*."""
    widget.setStyleSheet(SIDEBAR_QSS)

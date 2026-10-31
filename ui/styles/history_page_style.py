"""Stylesheet module for UI components.

Visual rules were extracted from the component files so the UI modules stay focused on behavior.
"""

HISTORY_PAGE_QSS = """
            /* PAGE */

            QWidget#history_page,
            QWidget#history_container,
            QScrollArea#history_scroll {
                background-color: #0b1120;
                border: none;
            }

            /* HERO */

            QFrame#history_hero {
                background: qlineargradient(
                    x1:0, y1:0,
                    x2:1, y2:1,
                    stop:0 #152e39,
                    stop:0.5 #122638,
                    stop:1 #151e38
                );
                border: 1px solid #294354;
                border-radius: 18px;
            }

            /* CARDS */

            QFrame#history_card,
            QFrame#history_stat_card {
                background-color: #141e30;
                border: 1px solid #29374c;
                border-radius: 16px;
            }

            /* HERO TYPOGRAPHY */

            QLabel#history_eyebrow {
                color: #5eead4;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 2px;
                background: transparent;
                border: none;
            }

            QLabel#history_hero_title {
                color: #f8fafc;
                font-family: "Segoe UI";
                font-size: 30px;
                font-weight: 800;
                background: transparent;
                border: none;
            }

            QLabel#history_description {
                color: #b8c5d5;
                font-family: "Segoe UI";
                font-size: 12px;
                background: transparent;
                border: none;
            }

            /* STATISTICS */

            QLabel#history_stat_title {
                color: #94a3b8;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
                background: transparent;
                border: none;
            }

            QLabel#history_stat_value {
                font-family: "Segoe UI";
                font-size: 30px;
                font-weight: 800;
                background: transparent;
                border: none;
            }

            QLabel#history_stat_value[category="total"] {
                color: #f1f5f9;
            }

            QLabel#history_stat_value[category="success"] {
                color: #5eead4;
            }

            QLabel#history_stat_value[category="failed"] {
                color: #fca5a5;
            }

            /* SECTION TITLES */

            QLabel#history_section_title {
                color: #f1f5f9;
                font-family: "Segoe UI";
                font-size: 19px;
                font-weight: 700;
                background: transparent;
                border: none;
            }

            QLabel#history_section_description {
                color: #94a3b8;
                font-family: "Segoe UI";
                font-size: 12px;
                background: transparent;
                border: none;
            }

            /* SEARCH */

            QLineEdit#history_search {
                background-color: #1b2940;
                color: #f1f5f9;
                border: 1px solid #304259;
                border-radius: 9px;
                padding: 8px 12px;
                font-family: "Segoe UI";
                font-size: 12px;
                selection-background-color: #285d60;
            }

            QLineEdit#history_search:focus {
                border: 1px solid #5eead4;
            }

            /* HISTORY LIST */

            QListWidget#history_list {
                background: transparent;
                border: none;
                outline: none;
            }

            QListWidget#history_list::item {
                background: transparent;
                border: none;
                padding: 0;
                margin: 0;
            }

            QListWidget#history_list::item:selected {
                background: transparent;
            }

            /* HISTORY RECORD */

            QFrame#history_record {
                background-color: #1b2940;
                border: 1px solid #304259;
                border-radius: 10px;
            }

            QFrame#history_record[selected="true"] {
                background-color: #173a40;
                border: 1px solid #5eead4;
                border-left: 3px solid #5eead4;
            }

            QLabel#history_record_name {
                color: #f1f5f9;
                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 700;
                background: transparent;
                border: none;
            }

            QLabel#history_record_metadata {
                color: #94a3b8;
                font-family: "Segoe UI";
                font-size: 11px;
                background: transparent;
                border: none;
            }

            /* STATUS BADGES */

            QLabel#history_status_badge,
            QLabel#history_detail_status {
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                padding: 5px 9px;
                border-radius: 7px;
            }

            QLabel#history_status_badge[status="success"],
            QLabel#history_detail_status[status="success"] {
                background-color: #173e43;
                color: #5eead4;
                border: 1px solid #28665f;
            }

            QLabel#history_status_badge[status="failed"],
            QLabel#history_detail_status[status="failed"] {
                background-color: #44252e;
                color: #fca5a5;
                border: 1px solid #75404c;
            }

            QLabel#history_status_badge[status="cancelled"],
            QLabel#history_detail_status[status="cancelled"] {
                background-color: #443820;
                color: #fcd34d;
                border: 1px solid #77602a;
            }

            QLabel#history_status_badge[status="unknown"],
            QLabel#history_detail_status[status="unknown"] {
                background-color: #263449;
                color: #94a3b8;
                border: 1px solid #394a61;
            }

            /* DETAILS */

            QWidget#history_details_container,
            QScrollArea#history_details_scroll {
                background: transparent;
                border: none;
            }

            QLabel#history_field_title {
                color: #64748b;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
                background: transparent;
                border: none;
            }

            QLabel#history_field_value {
                color: #d5deea;
                font-family: "Segoe UI";
                font-size: 12px;
                background: transparent;
                border: none;
            }

            /* ACTION BUTTONS */

            QPushButton#history_refresh_button {
                background-color: #5eead4;
                color: #0b1120;
                border: none;
                border-radius: 9px;
                padding: 8px 14px;
                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 700;
            }

            QPushButton#history_refresh_button:hover {
                background-color: #99f6e4;
            }

            QPushButton#history_refresh_button:pressed {
                background-color: #2dd4bf;
            }

            QPushButton#history_clear_button {
                background-color: #35232f;
                color: #fca5a5;
                border: 1px solid #75404c;
                border-radius: 9px;
                padding: 8px 14px;
                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 700;
            }

            QPushButton#history_clear_button:hover {
                background-color: #512c38;
                color: #fecaca;
            }

            QPushButton#history_clear_button:disabled {
                background-color: #202938;
                color: #64748b;
                border: 1px solid #29374c;
            }

            /* SCROLLBAR */

            QScrollBar:vertical {
                background: #141e30;
                width: 7px;
                margin: 0;
                border: none;
            }

            QScrollBar::handle:vertical {
                background: #334155;
                border-radius: 3px;
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


def apply_history_page_style(widget):
    """Apply the HISTORY_PAGE_QSS stylesheet to *widget*."""
    widget.setStyleSheet(HISTORY_PAGE_QSS)

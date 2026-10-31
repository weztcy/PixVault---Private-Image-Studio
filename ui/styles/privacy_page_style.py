"""Stylesheet module for UI components.

Visual rules were extracted from the component files so the UI modules stay focused on behavior.
"""

PRIVACY_PAGE_QSS = """
            QWidget#privacy_page,
            QWidget#privacy_container,
            QScrollArea#privacy_scroll {
                background-color: #0b1120;
                border: none;
            }

            QFrame#privacy_hero {
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

            QFrame#privacy_card {
                background-color: #141e30;
                border: 1px solid #29374c;
                border-radius: 16px;
            }

            QFrame#privacy_step {
                background-color: #1b2940;
                border: 1px solid #304259;
                border-radius: 12px;
            }

            QLabel#privacy_eyebrow {
                color: #5eead4;
                font-family: "Segoe UI";
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 2px;
            }

            QLabel#privacy_hero_title {
                color: #f8fafc;
                font-family: "Segoe UI";
                font-size: 34px;
                font-weight: 800;
            }

            QLabel#privacy_hero_description {
                color: #b8c5d5;
                font-family: "Segoe UI";
                font-size: 13px;
            }

            QLabel#privacy_status {
                color: #5eead4;
                background-color: #173e43;
                border: 1px solid #28665f;
                border-radius: 12px;
                padding: 8px 14px;
                font-family: "Segoe UI";
                font-size: 11px;
                font-weight: 700;
            }

            QLabel#privacy_shield {
                color: #5eead4;
                font-size: 70px;
                font-weight: 700;
            }

            QLabel#privacy_status_text {
                color: #9bb4c5;
                font-family: "Segoe UI";
                font-size: 11px;
            }

            QLabel#privacy_card_badge {
                color: #5eead4;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#privacy_card_title {
                color: #f1f5f9;
                font-family: "Segoe UI";
                font-size: 21px;
                font-weight: 700;
            }

            QLabel#privacy_card_description {
                color: #94a3b8;
                font-family: "Segoe UI";
                font-size: 12px;
            }

            QLabel#privacy_check_icon {
                color: #5eead4;
                background-color: #173c3e;
                border: 1px solid #285d56;
                border-radius: 14px;
                font-size: 14px;
                font-weight: 700;
            }

            QLabel#privacy_item_text {
                color: #d5deea;
                font-family: "Segoe UI";
                font-size: 12px;
            }

            QLabel#privacy_step_number {
                color: #5eead4;
                font-family: "Segoe UI";
                font-size: 20px;
                font-weight: 800;
            }

            QLabel#privacy_step_title {
                color: #f1f5f9;
                font-family: "Segoe UI";
                font-size: 14px;
                font-weight: 700;
            }

            QLabel#privacy_step_description {
                color: #94a3b8;
                font-family: "Segoe UI";
                font-size: 11px;
            }

            QLabel#privacy_footer_label {
                color: #64748b;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#privacy_footer_text {
                color: #64748b;
                font-family: "Segoe UI";
                font-size: 10px;
            }

            QScrollBar:vertical {
                background: #0b1120;
                width: 8px;
                margin: 0;
                border: none;
            }

            QScrollBar::handle:vertical {
                background: #334155;
                border-radius: 4px;
                min-height: 35px;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
                border: none;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
            """


def apply_privacy_page_style(widget):
    """Apply the PRIVACY_PAGE_QSS stylesheet to *widget*."""
    widget.setStyleSheet(PRIVACY_PAGE_QSS)

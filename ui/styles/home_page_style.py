"""Stylesheet module for UI components.

Visual rules were extracted from the component files so the UI modules stay focused on behavior.
"""

HOME_PAGE_QSS = """
            /* PAGE BACKGROUND */

            QWidget#home_page,
            QWidget#home_container,
            QScrollArea#home_scroll {
                background-color: #0b1120;
                border: none;
            }

            /* HERO CARD */

            QFrame#home_hero_card {
                background: qlineargradient(
                    x1:0, y1:0,
                    x2:1, y2:1,
                    stop:0 #15343b,
                    stop:0.5 #142b3b,
                    stop:1 #17213b
                );

                border: 1px solid #294b54;
                border-radius: 18px;
            }

            /* STANDARD CARDS */

            QFrame#home_card,
            QFrame#home_workflow_card {
                background-color: #141e30;
                border: 1px solid #29374c;
                border-radius: 16px;
            }

            /* TOOL ITEMS */

            QFrame#home_tool_item {
                background-color: #1b2940;
                border: 1px solid #304259;
                border-radius: 9px;
            }

            /* WORKFLOW STEPS */

            QFrame#home_workflow_step {
                background-color: #1b2940;
                border: 1px solid #304259;
                border-radius: 11px;
            }

            /* HERO EYEBROW */

            QLabel#home_eyebrow {
                color: #5eead4;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
                background: transparent;
                border: none;
            }

            /* MAIN TITLE */

            QLabel#home_hero_title {
                color: #f8fafc;
                font-family: "Segoe UI";
                font-size: 34px;
                font-weight: 800;
                background: transparent;
                border: none;
            }

            /* HERO SUBTITLE */

            QLabel#home_hero_subtitle {
                color: #e2e8f0;
                font-family: "Segoe UI";
                font-size: 18px;
                font-weight: 600;
                background: transparent;
                border: none;
            }

            /* HERO DESCRIPTION */

            QLabel#home_hero_description {
                color: #b8c5d5;
                font-family: "Segoe UI";
                font-size: 13px;
                background: transparent;
                border: none;
            }

            QLabel#home_hero_note {
                color: #8da9ad;
                font-family: "Segoe UI";
                font-size: 11px;
                background: transparent;
                border: none;
            }

            /* CARD BADGE */

            QLabel#home_card_badge {
                color: #5eead4;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
                background: transparent;
                border: none;
            }

            /* CARD TITLE */

            QLabel#home_card_title {
                color: #f1f5f9;
                font-family: "Segoe UI";
                font-size: 20px;
                font-weight: 700;
                background: transparent;
                border: none;
            }

            /* CARD DESCRIPTION */

            QLabel#home_card_description {
                color: #94a3b8;
                font-family: "Segoe UI";
                font-size: 12px;
                background: transparent;
                border: none;
            }

            /* CHECK ICON */

            QLabel#home_check_icon {
                color: #5eead4;
                background-color: #173c3e;
                border: 1px solid #285d56;
                border-radius: 13px;
                font-size: 13px;
                font-weight: 700;
            }

            /* PRIVACY ITEM TEXT */

            QLabel#home_item_text {
                color: #d5deea;
                font-family: "Segoe UI";
                font-size: 12px;
                background: transparent;
                border: none;
            }

            /* TOOL ICON */

            QLabel#home_tool_icon {
                color: #5eead4;
                font-family: "Segoe UI";
                font-size: 15px;
                font-weight: 700;
                background: transparent;
                border: none;
            }

            /* TOOL TEXT */

            QLabel#home_tool_text {
                color: #d5deea;
                font-family: "Segoe UI";
                font-size: 11px;
                font-weight: 500;
                background: transparent;
                border: none;
            }

            /* WORKFLOW NUMBER */

            QLabel#home_step_number {
                color: #5eead4;
                font-family: "Segoe UI";
                font-size: 19px;
                font-weight: 800;
                background: transparent;
                border: none;
            }

            /* WORKFLOW TITLE */

            QLabel#home_step_title {
                color: #f1f5f9;
                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: 700;
                background: transparent;
                border: none;
            }

            /* WORKFLOW DESCRIPTION */

            QLabel#home_step_description {
                color: #94a3b8;
                font-family: "Segoe UI";
                font-size: 11px;
                background: transparent;
                border: none;
            }

            /* START BUTTON */

            QPushButton#home_start_button {
                background-color: #5eead4;
                color: #0b1120;

                border: none;
                border-radius: 10px;

                padding: 10px 16px;

                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: 700;
            }

            QPushButton#home_start_button:hover {
                background-color: #99f6e4;
            }

            QPushButton#home_start_button:pressed {
                background-color: #2dd4bf;
            }

            /* FOOTER */

            QLabel#home_footer_label {
                color: #64748b;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                background: transparent;
                border: none;
            }

            QLabel#home_footer_text {
                color: #64748b;
                font-family: "Segoe UI";
                font-size: 10px;
                background: transparent;
                border: none;
            }

            /* SCROLLBAR */

            QScrollBar:vertical {
                background: #0b1120;
                width: 7px;
                margin: 0;
                border: none;
            }

            QScrollBar::handle:vertical {
                background: #334155;
                border-radius: 3px;
                min-height: 35px;
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


def apply_home_page_style(widget):
    """Apply the HOME_PAGE_QSS stylesheet to *widget*."""
    widget.setStyleSheet(HOME_PAGE_QSS)

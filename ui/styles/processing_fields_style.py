"""Stylesheet module for UI components.

Visual rules were extracted from the component files so the UI modules stay focused on behavior.
"""

CHECKBOX_GROUP_FIELD_QSS = """
            QLabel#checkbox_group_title {
                background: transparent; border: none; color: #CBD5E1;
                font-family: 'Segoe UI'; font-size: 12px; font-weight: 600;
            }
        """

FORMAT_SUPPORT_INFO_QSS = """
            /* =========================
               MAIN COMPONENT
            ========================= */

            QWidget#format_support_info {
                background: transparent;
                border: none;
            }

            /* =========================
               PREMIUM CARD
            ========================= */

            QFrame#format_support_card {
                background-color: #141e30;
                border: 1px solid #29374c;
                border-radius: 15px;
            }

            /* =========================
               HEADER EYEBROW
            ========================= */

            QLabel#support_eyebrow {
                color: #5eead4;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
            }

            /* =========================
               HEADER TITLE
            ========================= */

            QLabel#support_title {
                color: #f1f5f9;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 17px;
                font-weight: 700;
            }

            /* =========================
               HEADER DESCRIPTION
            ========================= */

            QLabel#support_description {
                color: #94a3b8;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 11px;
            }

            /* =========================
               FORMAT COUNT
            ========================= */

            QLabel#support_count {
                background-color: #173a40;
                color: #5eead4;

                border: 1px solid #28665f;
                border-radius: 8px;

                padding: 6px 12px;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
            }

            /* =========================
               SCROLL AREA
            ========================= */

            QScrollArea#format_support_scroll {
                background: transparent;
                border: none;
            }

            QWidget#format_support_container {
                background: transparent;
                border: none;
            }

            /* =========================
               FORMAT CARDS
            ========================= */

            QFrame#format_card {
                background-color: #1b2940;

                border: 1px solid #304259;
                border-radius: 10px;
            }

            QFrame#format_card:hover {
                background-color: #203b43;
                border: 1px solid #397d76;
            }

            /* =========================
               FORMAT INDICATOR
            ========================= */

            QLabel#format_indicator {
                color: #5eead4;

                background: transparent;
                border: none;

                font-family: "Segoe UI Symbol";
                font-size: 10px;
            }

            /* =========================
               FORMAT NAME
            ========================= */

            QLabel#format_name {
                color: #d5deea;

                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 700;
            }

            /* =========================
               SCROLL BUTTONS
            ========================= */

            QPushButton#format_scroll_button {
                background-color: #1b2940;

                color: #d5deea;

                border: 1px solid #304259;
                border-radius: 9px;

                font-family: "Segoe UI";
                font-size: 23px;
                font-weight: 600;

                padding: 0;
            }

            QPushButton#format_scroll_button:hover {
                background-color: #173a40;

                color: #5eead4;

                border: 1px solid #5eead4;
            }

            QPushButton#format_scroll_button:pressed {
                background-color: #285d60;
            }

            QPushButton#format_scroll_button:disabled {
                background-color: #192537;

                color: #475569;

                border: 1px solid #29374c;
            }

            /* =========================
               EMPTY STATE
            ========================= */

            QLabel#support_empty_label {
                color: #64748b;

                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 12px;

                padding: 8px;
            }

            /* =========================
               HORIZONTAL SCROLLBAR
            ========================= */

            QScrollBar:horizontal {
                background-color: #141e30;

                height: 7px;
                margin: 0;

                border: none;
            }

            QScrollBar::handle:horizontal {
                background-color: #334155;

                border-radius: 3px;
                min-width: 28px;
            }

            QScrollBar::handle:horizontal:hover {
                background-color: #5eead4;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0;
                border: none;
            }

            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {
                background: transparent;
            }
            """

NUMBER_FIELD_QSS = """
            QWidget#number_field { background: transparent; border: none; }
            QLabel#number_field_label {
                color: #CBD5E1; background: transparent; border: none;
                font-family: 'Segoe UI'; font-size: 12px; font-weight: 600;
            }
            QLabel#number_field_label:disabled { color: #64748B; }
            QSpinBox#premium_number_input {
                background-color: #1B2940; color: #F1F5F9;
                border: 1px solid #304259; border-radius: 10px;
                padding: 8px 13px; font-family: 'Segoe UI';
                font-size: 12px; font-weight: 600;
                selection-background-color: #173A40;
                selection-color: #5EEAD4;
            }
            QSpinBox#premium_number_input:hover { background-color: #203149; border-color: #426273; }
            QSpinBox#premium_number_input:focus { border-color: #5EEAD4; }
            QSpinBox#premium_number_input:disabled {
                background-color: #151E2D; color: #64748B; border-color: #253348;
            }
            QSpinBox#premium_number_input::up-button,
            QSpinBox#premium_number_input::down-button {
                background-color: #263449; border: none; width: 22px;
            }
            QSpinBox#premium_number_input::up-button:hover,
            QSpinBox#premium_number_input::down-button:hover { background-color: #173A40; }
        """


WARNING_LABEL_QSS = """
            QLabel#processing_warning {
                background-color: #443820; color: #FCD34D;
                border: 1px solid #77602A; border-radius: 8px;
                padding: 10px; font-family: 'Segoe UI'; font-size: 11px;
            }
        """


def apply_checkbox_group_field_style(widget):
    """Apply the CHECKBOX_GROUP_FIELD_QSS stylesheet to *widget*."""
    widget.setStyleSheet(CHECKBOX_GROUP_FIELD_QSS)

def apply_format_support_info_style(widget):
    """Apply the FORMAT_SUPPORT_INFO_QSS stylesheet to *widget*."""
    widget.setStyleSheet(FORMAT_SUPPORT_INFO_QSS)

def apply_number_field_style(widget):
    """Apply the NUMBER_FIELD_QSS stylesheet to *widget*."""
    widget.setStyleSheet(NUMBER_FIELD_QSS)

def apply_warning_label_style(widget):
    """Apply the WARNING_LABEL_QSS stylesheet to *widget*."""
    widget.setStyleSheet(WARNING_LABEL_QSS)

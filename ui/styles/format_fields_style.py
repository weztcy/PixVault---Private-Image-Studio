"""Stylesheet module for UI components.

Visual rules were extracted from the component files so the UI modules stay focused on behavior.
"""

CHECKBOX_FIELD_QSS = """
            /* =========================
               FIELD CONTAINER
            ========================= */

            QFrame#checkbox_field_container {
                background-color: #1b2940;
                border: 1px solid #304259;
                border-radius: 10px;
            }

            QFrame#checkbox_field_container:hover {
                background-color: #203149;
                border: 1px solid #426273;
            }

            /* =========================
               CHECKBOX TEXT
            ========================= */

            QCheckBox#premium_checkbox {
                background: transparent;
                border: none;

                color: #d5deea;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 500;

                spacing: 12px;
            }

            QCheckBox#premium_checkbox:hover {
                color: #f8fafc;
            }

            /* =========================
               UNCHECKED INDICATOR
            ========================= */

            QCheckBox#premium_checkbox::indicator {
                width: 18px;
                height: 18px;

                background-color: #101b2d;

                border: 1px solid #50647c;
                border-radius: 5px;
            }

            /* =========================
               INDICATOR HOVER
            ========================= */

            QCheckBox#premium_checkbox::indicator:hover {
                background-color: #263b4d;
                border: 1px solid #5eead4;
            }

            /* =========================
               CHECKED INDICATOR
            ========================= */

            QCheckBox#premium_checkbox::indicator:checked {
                background-color: #5eead4;
                border: 1px solid #5eead4;
                border-radius: 5px;
            }

            QCheckBox#premium_checkbox::indicator:checked:hover {
                background-color: #99f6e4;
                border: 1px solid #99f6e4;
            }

            /* =========================
               DISABLED STATE
            ========================= */

            QFrame#checkbox_field_container:disabled {
                background-color: #151e2d;
                border: 1px solid #253348;
            }

            QCheckBox#premium_checkbox:disabled {
                color: #64748b;
            }

            QCheckBox#premium_checkbox::indicator:disabled {
                background-color: #202b3b;
                border: 1px solid #354459;
            }

            /* =========================
               KEYBOARD FOCUS
            ========================= */

            QCheckBox#premium_checkbox::indicator:focus {
                border: 2px solid #5eead4;
            }
            """

DROPDOWN_FIELD_QSS = """
            /* =========================
               FIELD CONTAINER
            ========================= */

            QWidget#dropdown_field {
                background-color: transparent;
                border: none;
            }

            /* =========================
               FIELD LABEL
            ========================= */

            QLabel#dropdown_field_label {
                color: #cbd5e1;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 600;

                background: transparent;
                border: none;
            }

            /* =========================
               COMBO BOX
            ========================= */

            QComboBox#premium_dropdown {
                background-color: #1b2940;

                color: #f1f5f9;

                border: 1px solid #304259;
                border-radius: 10px;

                padding: 8px 44px 8px 14px;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 500;

                selection-background-color: #173a40;
                selection-color: #5eead4;
            }

            /* =========================
               HOVER
            ========================= */

            QComboBox#premium_dropdown:hover {
                background-color: #203149;

                border: 1px solid #426273;
            }

            /* =========================
               FOCUS
            ========================= */

            QComboBox#premium_dropdown:focus {
                background-color: #1c2e43;

                border: 1px solid #5eead4;
            }

            /* =========================
               DROP-DOWN AREA
            ========================= */

            QComboBox#premium_dropdown::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;

                width: 36px;

                background-color: transparent;

                border: none;
                border-left: 1px solid #304259;

                border-top-right-radius: 9px;
                border-bottom-right-radius: 9px;
            }

            QComboBox#premium_dropdown::down-arrow {
                image: none;

                width: 0px;
                height: 0px;
            }

            /* =========================
               DISABLED STATE
            ========================= */

            QComboBox#premium_dropdown:disabled {
                background-color: #151e2d;

                color: #64748b;

                border: 1px solid #253348;
            }

            /* =========================
               DROPDOWN LIST
            ========================= */

            QListView#premium_dropdown_view {
                background-color: #141e30;

                color: #d5deea;

                border: 1px solid #304259;

                outline: none;

                font-family: "Segoe UI";
                font-size: 12px;

                padding: 5px;
            }

            QListView#premium_dropdown_view::item {
                background-color: transparent;

                color: #d5deea;

                border: none;
                border-radius: 6px;

                padding: 9px 12px;

                min-height: 18px;
            }

            QListView#premium_dropdown_view::item:hover {
                background-color: #203149;

                color: #f8fafc;
            }

            QListView#premium_dropdown_view::item:selected {
                background-color: #173a40;

                color: #5eead4;
            }

            QListView#premium_dropdown_view::item:disabled {
                color: #64748b;
                background-color: transparent;
            }

            /* =========================
               POPUP SCROLLBAR
            ========================= */

            QListView#premium_dropdown_view QScrollBar:vertical {
                background-color: #141e30;

                width: 7px;
                margin: 0;

                border: none;
            }

            QListView#premium_dropdown_view QScrollBar::handle:vertical {
                background-color: #334155;

                border-radius: 3px;

                min-height: 25px;
            }

            QListView#premium_dropdown_view QScrollBar::handle:vertical:hover {
                background-color: #5eead4;
            }

            QListView#premium_dropdown_view QScrollBar::add-line:vertical,
            QListView#premium_dropdown_view QScrollBar::sub-line:vertical {
                height: 0;
                border: none;
            }

            QListView#premium_dropdown_view QScrollBar::add-page:vertical,
            QListView#premium_dropdown_view QScrollBar::sub-page:vertical {
                background: transparent;
            }
            """

RADIO_MODE_SELECTOR_QSS = """
            /* =========================
               MAIN CONTAINER
            ========================= */

            QWidget#radio_mode_selector {
                background-color: transparent;
                border: none;
            }

            /* =========================
               SECTION TITLE
            ========================= */

            QLabel#radio_selector_title {
                color: #cbd5e1;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 600;

                background: transparent;
                border: none;
            }

            /* =========================
               RADIO OPTION CARD
            ========================= */

            QRadioButton#premium_radio_option {
                background-color: #1b2940;

                color: #d5deea;

                border: 1px solid #304259;
                border-radius: 10px;

                padding: 10px 14px;

                spacing: 12px;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 500;
            }

            /* =========================
               HOVER STATE
            ========================= */

            QRadioButton#premium_radio_option:hover {
                background-color: #203149;

                color: #f8fafc;

                border: 1px solid #426273;
            }

            /* =========================
               SELECTED STATE
            ========================= */

            QRadioButton#premium_radio_option:checked {
                background-color: #173a40;

                color: #5eead4;

                border: 1px solid #397d76;
                border-left: 3px solid #5eead4;

                font-weight: 700;
            }

            /* =========================
               SELECTED HOVER
            ========================= */

            QRadioButton#premium_radio_option:checked:hover {
                background-color: #1c4649;

                color: #99f6e4;

                border: 1px solid #5eead4;
                border-left: 3px solid #5eead4;
            }

            /* =========================
               RADIO INDICATOR
            ========================= */

            QRadioButton#premium_radio_option::indicator {
                width: 18px;
                height: 18px;

                background-color: #101b2d;

                border: 2px solid #50647c;
                border-radius: 11px;
            }

            /* =========================
               INDICATOR HOVER
            ========================= */

            QRadioButton#premium_radio_option::indicator:hover {
                border: 2px solid #5eead4;

                background-color: #203149;
            }

            /* =========================
               CHECKED INDICATOR
            ========================= */

            QRadioButton#premium_radio_option::indicator:checked {
                background-color: #5eead4;

                border: 5px solid #173a40;

                border-radius: 11px;
            }

            /* =========================
               CHECKED INDICATOR HOVER
            ========================= */

            QRadioButton#premium_radio_option::indicator:checked:hover {
                background-color: #99f6e4;

                border: 5px solid #1c4649;
            }

            /* =========================
               PRESSED STATE
            ========================= */

            QRadioButton#premium_radio_option:pressed {
                background-color: #244b52;
            }

            /* =========================
               KEYBOARD FOCUS
            ========================= */

            QRadioButton#premium_radio_option:focus {
                border: 1px solid #5eead4;
            }

            QRadioButton#premium_radio_option:checked:focus {
                border: 1px solid #5eead4;
                border-left: 3px solid #5eead4;
            }

            /* =========================
               DISABLED STATE
            ========================= */

            QRadioButton#premium_radio_option:disabled {
                background-color: #151e2d;

                color: #64748b;

                border: 1px solid #253348;
            }

            QRadioButton#premium_radio_option::indicator:disabled {
                background-color: #202b3b;

                border: 2px solid #354459;
            }

            /* =========================
               DISABLED SELECTED
            ========================= */

            QRadioButton#premium_radio_option:checked:disabled {
                background-color: #192c32;

                color: #6b9c98;

                border: 1px solid #294c4d;
            }
            """

SLIDER_FIELD_QSS = """
            /* =========================
               MAIN COMPONENT
            ========================= */

            QWidget#slider_field {
                background: transparent;
                border: none;
            }

            /* =========================
               FIELD CONTAINER
            ========================= */

            QFrame#slider_field_container {
                background-color: #1b2940;

                border: 1px solid #304259;
                border-radius: 11px;
            }

            QFrame#slider_field_container:hover {
                background-color: #1e2d44;

                border: 1px solid #426273;
            }

            QFrame#slider_field_container:disabled {
                background-color: #151e2d;

                border: 1px solid #253348;
            }

            /* =========================
               FIELD TITLE
            ========================= */

            QLabel#slider_field_label {
                color: #d5deea;

                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 600;
            }

            QLabel#slider_field_label:disabled {
                color: #64748b;
            }

            /* =========================
               VALUE BADGE
            ========================= */

            QLabel#slider_value_badge {
                background-color: #173a40;

                color: #5eead4;

                border: 1px solid #285d60;
                border-radius: 8px;

                padding: 4px 10px;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 700;
            }

            QLabel#slider_value_badge:disabled {
                background-color: #202b3b;

                color: #64748b;

                border: 1px solid #354459;
            }

            /* =========================
               SLIDER BASE
            ========================= */

            QSlider#premium_slider {
                background: transparent;
                border: none;
            }

            /* =========================
               SLIDER TRACK
            ========================= */

            QSlider#premium_slider::groove:horizontal {
                background-color: #304259;

                height: 6px;

                border: none;
                border-radius: 3px;
            }

            /* =========================
               ACTIVE PROGRESS TRACK
            ========================= */

            QSlider#premium_slider::sub-page:horizontal {
                background-color: #5eead4;

                border: none;
                border-radius: 3px;
            }

            /* =========================
               INACTIVE TRACK
            ========================= */

            QSlider#premium_slider::add-page:horizontal {
                background-color: #304259;

                border: none;
                border-radius: 3px;
            }

            /* =========================
               SLIDER HANDLE
            ========================= */

            QSlider#premium_slider::handle:horizontal {
                background-color: #5eead4;

                border: 3px solid #101b2d;
                border-radius: 11px;

                width: 16px;
                height: 16px;

                margin: -8px 0;
            }

            /* =========================
               HANDLE HOVER
            ========================= */

            QSlider#premium_slider::handle:horizontal:hover {
                background-color: #99f6e4;

                border: 3px solid #173a40;
            }

            /* =========================
               HANDLE PRESSED
            ========================= */

            QSlider#premium_slider::handle:horizontal:pressed {
                background-color: #2dd4bf;

                border: 3px solid #285d60;
            }

            /* =========================
               KEYBOARD FOCUS
            ========================= */

            QSlider#premium_slider:focus::handle:horizontal {
                background-color: #99f6e4;

                border: 3px solid #285d60;
            }

            /* =========================
               DISABLED SLIDER
            ========================= */

            QSlider#premium_slider::groove:horizontal:disabled {
                background-color: #263348;
            }

            QSlider#premium_slider::sub-page:horizontal:disabled {
                background-color: #42615f;
            }

            QSlider#premium_slider::add-page:horizontal:disabled {
                background-color: #263348;
            }

            QSlider#premium_slider::handle:horizontal:disabled {
                background-color: #64748b;

                border: 3px solid #202b3b;
            }

            /* =========================
               MINIMUM / MAXIMUM LABELS
            ========================= */

            QLabel#slider_range_label {
                color: #64748b;

                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 500;
            }

            QLabel#slider_range_label:disabled {
                color: #475569;
            }
            """


def apply_checkbox_field_style(widget):
    """Apply the CHECKBOX_FIELD_QSS stylesheet to *widget*."""
    widget.setStyleSheet(CHECKBOX_FIELD_QSS)

def apply_dropdown_field_style(widget):
    """Apply the DROPDOWN_FIELD_QSS stylesheet to *widget*."""
    widget.setStyleSheet(DROPDOWN_FIELD_QSS)

def apply_radio_mode_selector_style(widget):
    """Apply the RADIO_MODE_SELECTOR_QSS stylesheet to *widget*."""
    widget.setStyleSheet(RADIO_MODE_SELECTOR_QSS)

def apply_slider_field_style(widget):
    """Apply the SLIDER_FIELD_QSS stylesheet to *widget*."""
    widget.setStyleSheet(SLIDER_FIELD_QSS)

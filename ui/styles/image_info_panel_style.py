"""Stylesheet module for UI components.

Visual rules were extracted from the component files so the UI modules stay focused on behavior.
"""

IMAGE_INFO_PANEL_QSS = """
            /* =========================
               MAIN WIDGET
            ========================= */

            QWidget#image_info_panel,
            QWidget#image_info_container,
            QScrollArea#image_info_scroll {
                background-color: transparent;
                border: none;
            }

            /* =========================
               PREMIUM HEADER
            ========================= */

            QFrame#image_info_header {
                background: qlineargradient(
                    x1:0, y1:0,
                    x2:1, y2:1,
                    stop:0 #15343b,
                    stop:0.5 #142b3b,
                    stop:1 #17213b
                );

                border: 1px solid #294b54;
                border-radius: 15px;
            }

            /* =========================
               HEADER ICON BOX
            ========================= */

            QFrame#image_info_icon_box {
                background-color: #173a40;
                border: 1px solid #285d60;
                border-radius: 12px;
            }

            QLabel#image_info_icon {
                background: transparent;
                border: none;

                color: #5eead4;

                font-family: "Segoe UI Symbol";
                font-size: 27px;
                font-weight: 700;
            }

            /* =========================
               HEADER TYPOGRAPHY
            ========================= */

            QLabel#image_info_eyebrow {
                color: #5eead4;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#image_info_title {
                color: #f8fafc;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 20px;
                font-weight: 700;
            }

            QLabel#image_info_description {
                color: #94a3b8;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 11px;
            }

            /* =========================
               MAIN INFORMATION CARD
            ========================= */

            QGroupBox#image_info_box {
                background-color: #141e30;

                border: 1px solid #29374c;
                border-radius: 15px;

                margin-top: 0;
                padding: 0;
            }

            /* =========================
               SECTION LABELS
            ========================= */

            QLabel#image_info_section_label {
                color: #94a3b8;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            /* =========================
               FILE NAME
            ========================= */

            QLabel#image_info_filename {
                color: #f1f5f9;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 18px;
                font-weight: 700;
            }

            /* =========================
               STATUS BADGE
            ========================= */

            QLabel#image_info_status {
                font-family: "Segoe UI";
                font-size: 9px;
                font-weight: 700;

                padding: 6px 10px;
                border-radius: 7px;
            }

            QLabel#image_info_status[
                image_state="empty"
            ] {
                background-color: #263449;
                color: #94a3b8;
                border: 1px solid #394a61;
            }

            QLabel#image_info_status[
                image_state="loaded"
            ] {
                background-color: #173e43;
                color: #5eead4;
                border: 1px solid #28665f;
            }

            QLabel#image_info_status[
                image_state="error"
            ] {
                background-color: #44252e;
                color: #fca5a5;
                border: 1px solid #75404c;
            }

            /* =========================
               DIVIDER
            ========================= */

            QFrame#image_info_divider {
                background-color: #29374c;
                border: none;
                min-height: 1px;
                max-height: 1px;
            }

            /* =========================
               STAT CARDS
            ========================= */

            QFrame#image_info_stat_card {
                background-color: #1b2940;

                border: 1px solid #304259;
                border-radius: 10px;
            }

            QLabel#image_info_stat_title {
                color: #64748b;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
            }

            QLabel#image_info_stat_value {
                color: #f1f5f9;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 14px;
                font-weight: 700;
            }

            QLabel#image_info_stat_value[
                field_type="image_info_format"
            ] {
                color: #5eead4;
            }

            /* =========================
               PROPERTY CARDS
            ========================= */

            QFrame#image_info_property_card {
                background-color: #19283c;

                border: 1px solid #304259;
                border-radius: 10px;
            }

            QLabel#image_info_property_title {
                color: #64748b;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
            }

            QLabel#image_info_property_value {
                color: #d5deea;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: 600;
            }

            /* =========================
               FILE PATH CARD
            ========================= */

            QFrame#image_info_path_card {
                background-color: #101b2d;

                border: 1px solid #304259;
                border-radius: 9px;
            }

            QLabel#image_info_path {
                color: #94a3b8;
                background: transparent;
                border: none;

                font-family: "Consolas";
                font-size: 11px;
            }

            /* =========================
               COPY PATH BUTTON
            ========================= */

            QPushButton#image_info_copy_button {
                background-color: #173a40;

                color: #5eead4;

                border: 1px solid #28665f;
                border-radius: 7px;

                padding: 6px 12px;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
            }

            QPushButton#image_info_copy_button:hover {
                background-color: #1c4649;

                color: #99f6e4;
                border: 1px solid #5eead4;
            }

            QPushButton#image_info_copy_button:pressed {
                background-color: #285d60;
            }

            QPushButton#image_info_copy_button:disabled {
                background-color: #202b3b;

                color: #64748b;
                border: 1px solid #354459;
            }

            /* =========================
               ERROR MESSAGE
            ========================= */

            QLabel#image_info_error {
                color: #fca5a5;

                background-color: #44252e;
                border: 1px solid #75404c;
                border-radius: 8px;

                padding: 10px;

                font-family: "Segoe UI";
                font-size: 11px;
            }

            /* =========================
               FOOTER
            ========================= */

            QLabel#image_info_footer_icon {
                color: #5eead4;
                background: transparent;
                border: none;

                font-size: 10px;
            }

            QLabel#image_info_footer_text {
                color: #64748b;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 10px;
            }

            /* =========================
               SCROLLBAR
            ========================= */

            QScrollBar:vertical {
                background: #0b1120;

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


def apply_image_info_panel_style(widget):
    """Apply the IMAGE_INFO_PANEL_QSS stylesheet to *widget*."""
    widget.setStyleSheet(IMAGE_INFO_PANEL_QSS)

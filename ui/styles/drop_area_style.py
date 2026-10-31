"""Stylesheet module for UI components.

Visual rules were extracted from the component files so the UI modules stay focused on behavior.
"""

DROP_AREA_QSS = """
            /* =========================
               DROP AREA
            ========================= */

            QWidget#drop_area {
                background-color: #141e30;

                border: 2px dashed #35526a;
                border-radius: 16px;
            }

            /* =========================
               HOVER
            ========================= */

            QWidget#drop_area:hover {
                background-color: #182b3c;

                border: 2px dashed #4d938b;
            }

            /* =========================
               DRAG ACTIVE
            ========================= */

            QWidget#drop_area[drag_active="true"] {
                background-color: #173a40;

                border: 2px dashed #5eead4;
            }

            /* =========================
               ICON CONTAINER
            ========================= */

            QFrame#drop_icon_container {
                background-color: #173a40;

                border: 1px solid #285d60;
                border-radius: 28px;
            }

            /* =========================
               UPLOAD ICON
            ========================= */

            QLabel#drop_upload_icon {
                background: transparent;
                border: none;

                color: #5eead4;

                font-family: "Segoe UI Symbol";
                font-size: 32px;
                font-weight: 700;
            }

            /* =========================
               TITLE
            ========================= */

            QLabel#drop_title {
                background: transparent;
                border: none;

                color: #f1f5f9;

                font-family: "Segoe UI";
                font-size: 16px;
                font-weight: 700;
            }

            /* =========================
               DESCRIPTION
            ========================= */

            QLabel#drop_description {
                background: transparent;
                border: none;

                color: #94a3b8;

                font-family: "Segoe UI";
                font-size: 12px;
            }

            /* =========================
               SUPPORTED FORMATS
            ========================= */

            QLabel#drop_formats {
                background: transparent;
                border: none;

                color: #64748b;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 500;
            }

            /* =========================
               BROWSE BUTTON
            ========================= */

            QPushButton#drop_browse_button {
                background-color: #5eead4;

                color: #0b1120;

                border: 1px solid #5eead4;
                border-radius: 9px;

                padding: 8px 18px;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 700;
            }

            QPushButton#drop_browse_button:hover {
                background-color: #99f6e4;
                border-color: #99f6e4;
            }

            QPushButton#drop_browse_button:pressed {
                background-color: #2dd4bf;
                border-color: #2dd4bf;
            }

            /* =========================
               FOLDER BUTTON
            ========================= */

            QPushButton#drop_folder_button {
                background-color: #1b2940;

                color: #d5deea;

                border: 1px solid #38536b;
                border-radius: 9px;

                padding: 8px 18px;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton#drop_folder_button:hover {
                background-color: #24384e;

                color: #f8fafc;

                border-color: #5eead4;
            }

            QPushButton#drop_folder_button:pressed {
                background-color: #173a40;

                color: #5eead4;
            }

            /* =========================
               KEYBOARD FOCUS
            ========================= */

            QPushButton#drop_browse_button:focus,
            QPushButton#drop_folder_button:focus {
                border: 2px solid #99f6e4;
            }

            /* =========================
               DISABLED
            ========================= */

            QPushButton#drop_browse_button:disabled,
            QPushButton#drop_folder_button:disabled {
                background-color: #202b3b;

                color: #64748b;

                border: 1px solid #354459;
            }
            """


def apply_drop_area_style(widget):
    """Apply the DROP_AREA_QSS stylesheet to *widget*."""
    widget.setStyleSheet(DROP_AREA_QSS)

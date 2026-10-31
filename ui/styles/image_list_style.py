"""Shared stylesheet for the virtualized ``ImageListWidget`` chrome.

Tile visuals (background, borders, icon, filename, metadata) are drawn
directly by ``ImageTileDelegate`` so thousands of rows stay cheap; only the
list chrome (card, header, buttons, scrollbar) needs a stylesheet.
"""

IMAGE_LIST_QSS = """
/* MAIN WIDGET */

QWidget#image_list_widget {
    background: transparent;
    border: none;
}

/* MAIN CARD */

QFrame#image_list_card {
    background-color: #141e30;
    border: 1px solid #29374c;
    border-radius: 16px;
}

/* HEADER */

QLabel#image_list_eyebrow {
    color: #5eead4;
    background: transparent;
    border: none;
    font-family: "Segoe UI";
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
}

QLabel#image_list_title {
    color: #f1f5f9;
    background: transparent;
    border: none;
    font-family: "Segoe UI";
    font-size: 19px;
    font-weight: 700;
}

QLabel#image_list_description {
    color: #94a3b8;
    background: transparent;
    border: none;
    font-family: "Segoe UI";
    font-size: 12px;
}

/* IMAGE COUNT */

QLabel#image_list_count {
    background-color: #173a40;
    color: #5eead4;
    border: 1px solid #28665f;
    border-radius: 8px;
    padding: 8px 12px;
    font-family: "Segoe UI";
    font-size: 10px;
    font-weight: 700;
}

/* VIRTUAL LIST */

QListWidget#image_list_scroll {
    background: transparent;
    border: none;
}

QListWidget#image_list_scroll::item {
    background: transparent;
    border: none;
    margin: 0;
}

/* EMPTY STATE */

QFrame#image_list_empty_state {
    background-color: #111b2b;
    border: 1px dashed #36546b;
    border-radius: 12px;
}

QLabel#image_list_empty_icon {
    color: #5eead4;
    background: transparent;
    border: none;
    font-family: "Segoe UI Symbol";
    font-size: 33px;
}

QLabel#image_list_empty_title {
    color: #f1f5f9;
    background: transparent;
    border: none;
    font-family: "Segoe UI";
    font-size: 14px;
    font-weight: 700;
}

QLabel#image_list_empty_description {
    color: #64748b;
    background: transparent;
    border: none;
    font-family: "Segoe UI";
    font-size: 11px;
}

/* SELECTION STATUS */

QLabel#image_list_selection_icon {
    color: #5eead4;
    background: transparent;
    border: none;
    font-size: 9px;
}

QLabel#image_list_selection_text {
    color: #94a3b8;
    background: transparent;
    border: none;
    font-family: "Segoe UI";
    font-size: 11px;
}

/* SORT BUTTON */

QPushButton#image_list_sort_button {
    background-color: #1b2940;
    color: #d5deea;
    border: 1px solid #38536b;
    border-radius: 9px;
    padding: 8px 12px;
    font-family: "Segoe UI";
    font-size: 12px;
    font-weight: 600;
}

QPushButton#image_list_sort_button:hover {
    background-color: #24384e;
    color: #f8fafc;
    border-color: #5eead4;
}

/* REMOVE BUTTON */

QPushButton#image_list_remove_button {
    background-color: #173a40;
    color: #5eead4;
    border: 1px solid #28665f;
    border-radius: 9px;
    padding: 8px 12px;
    font-family: "Segoe UI";
    font-size: 12px;
    font-weight: 700;
}

QPushButton#image_list_remove_button:hover {
    background-color: #1c4649;
    color: #99f6e4;
    border-color: #5eead4;
}

/* CLEAR BUTTON */

QPushButton#image_list_clear_button {
    background-color: #35232f;
    color: #fca5a5;
    border: 1px solid #75404c;
    border-radius: 9px;
    padding: 8px 12px;
    font-family: "Segoe UI";
    font-size: 12px;
    font-weight: 700;
}

QPushButton#image_list_clear_button:hover {
    background-color: #512c38;
    color: #fecaca;
}

/* BUTTON PRESSED */

QPushButton#image_list_sort_button:pressed,
QPushButton#image_list_remove_button:pressed {
    background-color: #285d60;
}

QPushButton#image_list_clear_button:pressed {
    background-color: #663440;
}

/* DISABLED BUTTONS */

QPushButton#image_list_sort_button:disabled,
QPushButton#image_list_remove_button:disabled,
QPushButton#image_list_clear_button:disabled {
    background-color: #202b3b;
    color: #64748b;
    border: 1px solid #354459;
}

/* SORT POPUP */

QMenu#image_list_sort_menu {
    background-color: #141e30;
    color: #d5deea;
    border: 1px solid #304259;
    border-radius: 9px;
    padding: 6px;
    font-family: "Segoe UI";
    font-size: 12px;
}

QMenu#image_list_sort_menu::item {
    padding: 9px 22px;
    border-radius: 6px;
}

QMenu#image_list_sort_menu::item:selected {
    background-color: #173a40;
    color: #5eead4;
}

/* VERTICAL SCROLLBAR */

QScrollBar:vertical {
    background-color: #141e30;
    width: 7px;
    margin: 0;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #334155;
    border-radius: 3px;
    min-height: 28px;
}

QScrollBar::handle:vertical:hover {
    background-color: #5eead4;
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


def apply_image_list_style(widget):
    """Apply the ImageListWidget chrome stylesheet to *widget*."""
    widget.setStyleSheet(IMAGE_LIST_QSS)
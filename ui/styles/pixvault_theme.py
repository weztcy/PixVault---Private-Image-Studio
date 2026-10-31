"""Reusable PixVault page styles (dark navy + emerald).

Give a widget the ``pvRole`` dynamic property to opt in to a style.
This avoids overriding the existing QSS of reusable components.
"""

COLORS = {
    "background": "#0B1120",
    "surface": "#141E30",
    "surface_alt": "#1B2940",
    "border": "#29374C",
    "text": "#F1F5F9",
    "muted": "#94A3B8",
    "emerald": "#5EEAD4",
}

PAGE_THEME_QSS = """
/* MAIN PAGE & SCROLL CONTAINER */
QWidget[pvRole="page"],
QWidget[pvRole="pageContainer"],
QScrollArea[pvRole="pageScroll"] {
    background-color: #0B1120;
    border: none;
}

/* REUSABLE SURFACES */
QFrame[pvRole="hero"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #15343B, stop:0.5 #142B3B, stop:1 #17213B);
    border: 1px solid #294B54;
    border-radius: 18px;
}
QFrame[pvRole="card"],
QWidget[pvRole="detailPanel"] {
    background-color: #141E30;
    border: 1px solid #29374C;
    border-radius: 16px;
}
QGroupBox[pvRole="infoBody"] {
    background: transparent;
    border: none;
    margin: 0;
    padding: 0;
}
QFrame[pvRole="miniCard"] {
    background-color: #1B2940;
    border: 1px solid #304259;
    border-radius: 10px;
}
QFrame[pvRole="pathCard"] {
    background-color: #101B2D;
    border: 1px solid #304259;
    border-radius: 9px;
}
QFrame[pvRole="divider"] {
    background-color: #29374C;
    border: none;
    min-height: 1px;
    max-height: 1px;
}

/* TEXT ROLES */
QLabel[pvRole="eyebrow"] {
    background: transparent; border: none;
    color: #5EEAD4; font-family: "Segoe UI";
    font-size: 10px; font-weight: 700;
}
QLabel[pvRole="heroTitle"] {
    background: transparent; border: none;
    color: #F8FAFC; font-family: "Segoe UI";
    font-size: 30px; font-weight: 800;
}
QLabel[pvRole="heroDescription"] {
    background: transparent; border: none;
    color: #B8C5D5; font-family: "Segoe UI";
    font-size: 12px;
}
QLabel[pvRole="sectionTitle"],
QLabel[pvRole="cardTitle"] {
    background: transparent; border: none;
    color: #F1F5F9; font-family: "Segoe UI";
    font-size: 18px; font-weight: 700;
}
QLabel[pvRole="description"],
QLabel[pvRole="sectionDescription"] {
    background: transparent; border: none;
    color: #94A3B8; font-family: "Segoe UI";
    font-size: 12px;
}
QLabel[pvRole="fieldTitle"],
QLabel[pvRole="miniTitle"] {
    background: transparent; border: none;
    color: #94A3B8; font-family: "Segoe UI";
    font-size: 10px; font-weight: 700;
}
QLabel[pvRole="fieldValue"],
QLabel[pvRole="miniValue"] {
    background: transparent; border: none;
    color: #F1F5F9; font-family: "Segoe UI";
    font-size: 12px; font-weight: 600;
}
QLabel[pvRole="filename"] {
    background: transparent; border: none;
    color: #F1F5F9; font-family: "Segoe UI";
    font-size: 16px; font-weight: 700;
}
QLabel[pvRole="pathValue"] {
    background: transparent; border: none;
    color: #CBD5E1; font-family: "Consolas";
    font-size: 11px;
}
QLabel[pvRole="hint"] {
    background: transparent; border: none;
    color: #64748B; font-family: "Segoe UI";
    font-size: 11px;
}
QLabel[pvRole="errorText"] {
    background-color: #44252E;
    color: #FCA5A5;
    border: 1px solid #75404C;
    border-radius: 8px;
    padding: 10px;
    font-family: "Segoe UI";
    font-size: 11px;
}

/* LABEL BADGES */
QLabel[pvRole="countBadge"],
QLabel[pvRole="sectionNumber"] {
    background-color: #173A40;
    color: #5EEAD4;
    border: 1px solid #28665F;
    border-radius: 9px;
    padding: 7px 11px;
    font-family: "Segoe UI";
    font-size: 10px;
    font-weight: 700;
}
QLabel[pvRole="sectionNumber"] {
    font-size: 14px;
    padding: 0;
}
QLabel[pvRole="statusBadge"] {
    background-color: #263449;
    color: #94A3B8;
    border: 1px solid #394A61;
    border-radius: 8px;
    padding: 7px 11px;
    font-family: "Segoe UI";
    font-size: 10px;
    font-weight: 700;
}
QLabel[pvRole="statusBadge"][state="processing"],
QLabel[pvRole="statusBadge"][state="completed"],
QLabel[pvRole="statusBadge"][state="loaded"] {
    background-color: #173E43;
    color: #5EEAD4;
    border-color: #28665F;
}
QLabel[pvRole="statusBadge"][state="failed"],
QLabel[pvRole="statusBadge"][state="error"] {
    background-color: #44252E;
    color: #FCA5A5;
    border-color: #75404C;
}
QLabel[pvRole="statusBadge"][state="cancelled"] {
    background-color: #443820;
    color: #FCD34D;
    border-color: #77602A;
}

/* FORM FIELDS */
QComboBox[pvRole="field"] {
    background-color: #1B2940;
    color: #F1F5F9;
    border: 1px solid #304259;
    border-radius: 10px;
    padding: 9px 14px;
    font-family: "Segoe UI";
    font-size: 12px;
    font-weight: 600;
}
QComboBox[pvRole="field"]:hover {
    background-color: #203149;
    border-color: #426273;
}
QComboBox[pvRole="field"]:focus { border-color: #5EEAD4; }
QComboBox[pvRole="field"]::drop-down {
    width: 32px;
    border: none;
    border-left: 1px solid #304259;
    background: transparent;
}
QComboBox[pvRole="field"] QAbstractItemView {
    background-color: #141E30;
    color: #D5DEEA;
    border: 1px solid #304259;
    selection-background-color: #173A40;
    selection-color: #5EEAD4;
    outline: none;
}
QComboBox[pvRole="field"]:disabled {
    background-color: #151E2D;
    color: #64748B;
    border-color: #253348;
}

/* BUTTONS */
QPushButton[pvRole="primaryButton"] {
    background-color: #5EEAD4;
    color: #0B1120;
    border: 1px solid #5EEAD4;
    border-radius: 10px;
    padding: 10px 19px;
    font-family: "Segoe UI";
    font-size: 12px;
    font-weight: 700;
}
QPushButton[pvRole="primaryButton"]:hover {
    background-color: #99F6E4;
    border-color: #99F6E4;
}
QPushButton[pvRole="primaryButton"]:pressed {
    background-color: #2DD4BF;
    border-color: #2DD4BF;
}
QPushButton[pvRole="primaryButton"]:disabled {
    background-color: #263449;
    color: #64748B;
    border-color: #394A61;
}
QPushButton[pvRole="secondaryButton"] {
    background-color: #173A40;
    color: #5EEAD4;
    border: 1px solid #28665F;
    border-radius: 9px;
    padding: 8px 14px;
    font-family: "Segoe UI";
    font-size: 11px;
    font-weight: 700;
}
QPushButton[pvRole="secondaryButton"]:hover {
    background-color: #1C4649;
    border-color: #5EEAD4;
}
QPushButton[pvRole="secondaryButton"]:disabled {
    background-color: #202B3B;
    color: #64748B;
    border-color: #354459;
}
QPushButton[pvRole="dangerButton"] {
    background-color: #35232F;
    color: #FCA5A5;
    border: 1px solid #75404C;
    border-radius: 10px;
    padding: 10px 17px;
    font-family: "Segoe UI";
    font-size: 12px;
    font-weight: 700;
}
QPushButton[pvRole="dangerButton"]:hover {
    background-color: #512C38;
    color: #FECACA;
}
QPushButton[pvRole="dangerButton"]:disabled {
    background-color: #202B3B;
    color: #64748B;
    border-color: #354459;
}

/* ONLY THE OUTER PAGE SCROLLBAR */
QScrollArea[pvRole="pageScroll"] QScrollBar:vertical {
    background-color: #0B1120;
    width: 7px;
    margin: 0;
    border: none;
}
QScrollArea[pvRole="pageScroll"] QScrollBar::handle:vertical {
    background-color: #334155;
    border-radius: 3px;
    min-height: 30px;
}
QScrollArea[pvRole="pageScroll"] QScrollBar::handle:vertical:hover {
    background-color: #5EEAD4;
}
QScrollArea[pvRole="pageScroll"] QScrollBar::add-line:vertical,
QScrollArea[pvRole="pageScroll"] QScrollBar::sub-line:vertical {
    height: 0;
    border: none;
}
QScrollArea[pvRole="pageScroll"] QScrollBar::add-page:vertical,
QScrollArea[pvRole="pageScroll"] QScrollBar::sub-page:vertical {
    background: transparent;
}
"""


def role(widget, name):
    """Mark a widget with a reusable visual role."""
    widget.setProperty("pvRole", name)
    return widget


def apply_page_theme(widget):
    """Apply shared roles/styles to any PixVault QWidget page or component."""
    widget.setStyleSheet(PAGE_THEME_QSS)

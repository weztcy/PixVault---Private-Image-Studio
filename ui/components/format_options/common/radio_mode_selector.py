from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QLabel,
    QRadioButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ui.styles.format_fields_style import apply_radio_mode_selector_style


class RadioModeSelector(QWidget):
    mode_changed = Signal(str)

    def __init__(
        self,
        title,
        modes,
        default=None,
    ):
        super().__init__()

        self.setObjectName("radio_mode_selector")

        self.buttons = {}
        self.group = QButtonGroup(self)
        self.group.setExclusive(True)

        self.setup_ui(
            title,
            modes,
            default,
        )

        self.apply_styles()

    # =====================
    # USER INTERFACE
    # =====================

    def setup_ui(
        self,
        title,
        modes,
        default,
    ):
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.setSpacing(10)

        # =====================
        # SECTION TITLE
        # =====================

        self.title_label = QLabel(title)

        self.title_label.setObjectName("radio_selector_title")

        self.title_label.setWordWrap(True)

        main_layout.addWidget(self.title_label)

        main_layout.addSpacing(3)

        # =====================
        # RADIO OPTIONS
        # =====================

        self.options_layout = QVBoxLayout()

        self.options_layout.setSpacing(8)

        self.options_layout.setContentsMargins(0, 0, 0, 0)

        for mode in modes:
            button = self.create_radio_option(mode)

            self.buttons[mode] = button

            self.group.addButton(button)

            self.options_layout.addWidget(button)

            button.toggled.connect(
                lambda checked, value=mode: self.changed(checked, value)
            )

        main_layout.addLayout(self.options_layout)

        # =====================
        # DEFAULT SELECTION
        # =====================

        if default is not None and default in self.buttons:
            self.buttons[default].setChecked(True)

    # =====================
    # RADIO OPTION FACTORY
    # =====================

    def create_radio_option(self, mode):
        button = QRadioButton(str(mode))

        button.setObjectName("premium_radio_option")

        button.setMinimumHeight(48)

        button.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        button.setCursor(Qt.CursorShape.PointingHandCursor)

        button.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        button.setAccessibleName(str(mode))

        return button

    # =====================
    # MODE CHANGED
    # =====================

    def changed(
        self,
        checked,
        mode,
    ):
        if checked:
            self.mode_changed.emit(str(mode))

    # =====================
    # GET CURRENT VALUE
    # =====================

    def value(self):
        for name, button in self.buttons.items():
            if button.isChecked():
                return name

        return None

    # =====================
    # SET CURRENT VALUE
    # =====================

    def set_value(self, value):
        if value in self.buttons:
            self.buttons[value].setChecked(True)

    # =====================
    # PREMIUM STYLING
    # =====================

    def apply_styles(self):
        apply_radio_mode_selector_style(self)

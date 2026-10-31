from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from ui.styles.format_fields_style import apply_slider_field_style


class SliderField(QWidget):
    value_changed = Signal(int)

    def __init__(
        self,
        title,
        minimum,
        maximum,
        default,
    ):
        super().__init__()

        self.setObjectName("slider_field")

        self.title = title

        self.setup_ui(
            minimum,
            maximum,
            default,
        )

        self.apply_styles()

    # =====================
    # USER INTERFACE
    # =====================

    def setup_ui(
        self,
        minimum,
        maximum,
        default,
    ):
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # =====================
        # FIELD CONTAINER
        # =====================

        self.container = QFrame()
        self.container.setObjectName("slider_field_container")

        self.container.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        container_layout = QVBoxLayout(self.container)

        container_layout.setContentsMargins(16, 14, 16, 12)
        container_layout.setSpacing(12)

        # =====================
        # HEADER
        # =====================

        header_layout = QHBoxLayout()

        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)

        # Field Title

        self.label = QLabel(str(self.title))

        self.label.setObjectName("slider_field_label")

        self.label.setWordWrap(True)

        # Current Value Badge

        self.value_label = QLabel("0")

        self.value_label.setObjectName("slider_value_badge")

        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.value_label.setMinimumWidth(48)
        self.value_label.setMinimumHeight(30)

        # Header Assembly

        header_layout.addWidget(
            self.label,
            1,
        )

        header_layout.addWidget(
            self.value_label,
            0,
        )

        container_layout.addLayout(header_layout)

        # =====================
        # PREMIUM SLIDER
        # =====================

        self.slider = QSlider(Qt.Orientation.Horizontal)

        self.slider.setObjectName("premium_slider")

        self.slider.setRange(
            minimum,
            maximum,
        )

        self.slider.setMinimumHeight(30)

        self.slider.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.slider.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.slider.setTickPosition(QSlider.TickPosition.NoTicks)

        self.slider.setCursor(Qt.CursorShape.PointingHandCursor)

        self.slider.setAccessibleName(str(self.title))

        self.label.setBuddy(self.slider)

        # Set initial value before connecting
        # the signal to avoid initial emission.

        self.slider.setValue(default)

        self.value_label.setText(str(self.slider.value()))

        container_layout.addWidget(self.slider)

        # =====================
        # RANGE INDICATORS
        # =====================

        range_layout = QHBoxLayout()

        range_layout.setContentsMargins(2, 0, 2, 0)
        range_layout.setSpacing(8)

        self.minimum_label = QLabel(str(self.slider.minimum()))

        self.minimum_label.setObjectName("slider_range_label")

        self.maximum_label = QLabel(str(self.slider.maximum()))

        self.maximum_label.setObjectName("slider_range_label")

        self.maximum_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        range_layout.addWidget(self.minimum_label)

        range_layout.addStretch()

        range_layout.addWidget(self.maximum_label)

        container_layout.addLayout(range_layout)

        # =====================
        # ASSEMBLE COMPONENT
        # =====================

        main_layout.addWidget(self.container)

        # =====================
        # SIGNAL CONNECTION
        # =====================

        self.slider.valueChanged.connect(self.update_value)

        self.update_tooltip(self.slider.value())

    # =====================
    # VALUE CHANGED
    # =====================

    def update_value(self, value):
        self.value_label.setText(str(value))

        self.update_tooltip(value)

        self.value_changed.emit(value)

    # =====================
    # TOOLTIP
    # =====================

    def update_tooltip(self, value):
        self.slider.setToolTip(f"{self.title}: {value}")

    # =====================
    # GET CURRENT VALUE
    # =====================

    def value(self):
        return self.slider.value()

    # =====================
    # SET CURRENT VALUE
    # =====================

    def set_value(self, value):
        self.slider.setValue(int(value))

    # =====================
    # OPTIONAL RANGE UPDATE
    # =====================

    def set_range(
        self,
        minimum,
        maximum,
    ):
        self.slider.setRange(
            minimum,
            maximum,
        )

        self.minimum_label.setText(str(self.slider.minimum()))

        self.maximum_label.setText(str(self.slider.maximum()))

        self.value_label.setText(str(self.slider.value()))

        self.update_tooltip(self.slider.value())

    # =====================
    # PREMIUM STYLING
    # =====================

    def apply_styles(self):
        apply_slider_field_style(self)

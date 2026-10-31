from PySide6.QtCore import (
    QPointF,
    Qt,
    Signal,
)
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListView,
    QVBoxLayout,
    QWidget,
)

# =====================
# PREMIUM COMBO BOX
# =====================
from ui.styles.format_fields_style import apply_dropdown_field_style


class PremiumComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("premium_dropdown")

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.setMinimumHeight(44)

        self.setMaxVisibleItems(10)

        # Custom dropdown list

        view = QListView(self)

        view.setObjectName("premium_dropdown_view")

        view.setFrameShape(QListView.Shape.NoFrame)

        view.setSpacing(2)

        view.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        self.setView(view)

        self.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon
        )

        self.setMinimumContentsLength(12)

    # =====================
    # CUSTOM ARROW
    # =====================

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if not self.isEnabled():
            arrow_color = QColor("#64748b")

        elif self.hasFocus() or self.underMouse():
            arrow_color = QColor("#5eead4")

        else:
            arrow_color = QColor("#94a3b8")

        pen = QPen(arrow_color)
        pen.setWidthF(1.8)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)

        painter.setPen(pen)

        center_x = self.width() - 19
        center_y = self.height() / 2

        painter.drawLine(
            QPointF(center_x - 5, center_y - 2),
            QPointF(center_x, center_y + 3),
        )

        painter.drawLine(
            QPointF(center_x, center_y + 3),
            QPointF(center_x + 5, center_y - 2),
        )

        painter.end()


# =====================
# DROPDOWN FIELD
# =====================


class DropdownField(QWidget):
    value_changed = Signal(str)

    def __init__(
        self,
        title,
        items,
        default=None,
    ):
        super().__init__()

        self.setObjectName("dropdown_field")

        self.setup_ui(
            title,
            items,
            default,
        )

        self.apply_styles()

    # =====================
    # USER INTERFACE
    # =====================

    def setup_ui(
        self,
        title,
        items,
        default,
    ):
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.setSpacing(9)

        # =====================
        # FIELD LABEL
        # =====================

        header_layout = QHBoxLayout()

        header_layout.setContentsMargins(2, 0, 2, 0)

        header_layout.setSpacing(8)

        self.label = QLabel(title)

        self.label.setObjectName("dropdown_field_label")

        self.label.setWordWrap(True)

        header_layout.addWidget(self.label)

        header_layout.addStretch()

        # =====================
        # COMBO BOX
        # =====================

        self.combo = PremiumComboBox()

        self.combo.setAccessibleName(str(title))

        self.combo.addItems(items)

        if default is not None:
            self.combo.setCurrentText(str(default))

        # =====================
        # ASSEMBLE LAYOUT
        # =====================

        main_layout.addLayout(header_layout)

        main_layout.addWidget(self.combo)

        # =====================
        # SIGNAL CONNECTION
        # =====================

        self.combo.currentTextChanged.connect(self.value_changed.emit)

    # =====================
    # GET VALUE
    # =====================

    def value(self):
        return self.combo.currentText()

    # =====================
    # SET VALUE
    # =====================

    def set_value(self, value):
        self.combo.setCurrentText(str(value))

    # =====================
    # PREMIUM STYLING
    # =====================

    def apply_styles(self):
        apply_dropdown_field_style(self)

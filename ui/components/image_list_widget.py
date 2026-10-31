"""Virtualized image collection list for the PixVault workspaces.

Rows render through a ``QStyledItemDelegate`` backed by one lightweight
model item per file (no child widget per file), so importing and scrolling
through thousands of images stays responsive.
"""

from pathlib import Path

from PySide6.QtCore import QEvent, QRect, QRectF, QSize, Qt, QTimer, Signal
from PySide6.QtGui import (
    QColor,
    QFont,
    QFontMetrics,
    QPainter,
    QPainterPath,
    QPen,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QBoxLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListView,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QPushButton,
    QSizePolicy,
    QStyle,
    QStyledItemDelegate,
    QVBoxLayout,
    QWidget,
)

from ui.styles.image_list_style import apply_image_list_style

ICON_GLYPH = "\u25a7"
SORT_GLYPH = "↕"
REMOVE_GLYPH = "✖"
SELECTION_GLYPH = "●"

COLUMNS = 4
GRID_SPACING = 10
TILE_HEIGHT = 70


def index_text(index):
    return f"FILE {index + 1:02d}"




class ImageTileDelegate(QStyledItemDelegate):
    """Paint each tile directly with no per-file widget overhead."""

    def __init__(self, owner):
        super().__init__(owner)
        self.owner = owner

    def sizeHint(self, option, index):
        return QSize(
            self.owner.calculate_tile_width(),
            TILE_HEIGHT
        )

    def paint(self, painter, option, index):
        row = index.row()
        images = self.owner.images
        if not 0 <= row < len(images):
            return
        image = images[row]

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        rect = option.rect.adjusted(
            GRID_SPACING // 2,
            2,
            -GRID_SPACING // 2,
            -2
        )
        hovered = bool(option.state & QStyle.StateFlag.State_MouseOver)
        selected = self.owner.selected_index == row

        if selected:
            background, border, width = QColor("#173a40"), QColor("#5eead4"), 2
        elif hovered:
            background, border, width = QColor("#21334a"), QColor("#426273"), 1
        else:
            background, border, width = QColor("#1b2940"), QColor("#304259"), 1

        tile_path = QPainterPath()
        tile_path.addRoundedRect(QRectF(rect), 11, 11)
        painter.fillPath(tile_path, background)
        painter.setPen(QPen(border, width))
        painter.drawPath(tile_path)

        # File icon box
        icon_rect = QRect(rect.left() + 12, rect.center().y() - 20, 36, 40)
        icon_path = QPainterPath()
        icon_path.addRoundedRect(QRectF(icon_rect), 9, 9)
        painter.fillPath(icon_path, QColor("#173a40"))
        painter.setPen(QPen(QColor("#285d60"), 1))
        painter.drawPath(icon_path)

        icon_font = QFont("Segoe UI Symbol")
        icon_font.setPixelSize(23)
        icon_font.setBold(True)
        painter.setFont(icon_font)
        painter.setPen(QColor("#5eead4"))
        painter.drawText(icon_rect, Qt.AlignmentFlag.AlignCenter, ICON_GLYPH)

        text_left = rect.left() + 58
        available = max(20, rect.right() - 12 - text_left)

        name_font = QFont("Segoe UI")
        name_font.setPixelSize(12)
        name_font.setWeight(QFont.Weight.DemiBold)
        painter.setFont(name_font)
        painter.setPen(QColor("#f1f5f9"))
        name = QFontMetrics(name_font).elidedText(
            image.name, Qt.TextElideMode.ElideMiddle, available
        )
        painter.drawText(text_left, rect.top() + 30, name)

        extension = image.suffix.lstrip(".").upper() or "IMAGE"
        meta_font = QFont("Segoe UI")
        meta_font.setPixelSize(10)
        painter.setFont(meta_font)
        painter.setPen(QColor("#94a3b8"))
        painter.drawText(
            text_left,
            rect.top() + 50,
            f"{extension}  \u2022  {index_text(row)}",
        )

        painter.restore()


class ImageListWidget(QWidget):
    image_selected = Signal(Path)
    images_changed = Signal(list)

    COLUMNS = COLUMNS
    GRID_SPACING = GRID_SPACING

    def calculate_tile_width(self):
        if not hasattr(self, "list"):
            return 120

        vp_w = self.list.viewport().width()
        if vp_w <= 0:
            return 120

        cell_width = max((vp_w - 2) // COLUMNS, 60)
        return max(cell_width - GRID_SPACING, 50)

    def update_grid_size(self):
        if not hasattr(self, "list"):
            return

        vp_w = self.list.viewport().width()
        if vp_w <= 0:
            return

        # Divide viewport evenly across exactly COLUMNS (4) so the cards
        # span the full width of the container without trailing empty space.
        cell_width = max((vp_w - 2) // COLUMNS, 60)
        cell_height = TILE_HEIGHT + GRID_SPACING

        self.list.setGridSize(
            QSize(
                cell_width,
                cell_height,
            )
        )
        # Force the view to re-flow items immediately so the new grid
        # takes effect for item placement and painting.
        self.list.doItemsLayout()

        self.list.viewport().update()


    def __init__(self):
        super().__init__()

        self.images = []
        self.selected_index = None
        self.selected_image = None

        # The list viewport gets its real size after the surrounding layout
        # pass; debounce so the grid follows the actual viewport width.
        self._grid_timer = QTimer(self)
        self._grid_timer.setSingleShot(True)
        self._grid_timer.setInterval(0)
        self._grid_timer.timeout.connect(self.update_grid_size)

        self.setObjectName("image_list_widget")

        self.setup_ui()
        self.apply_styles()
        self.refresh()

    # =====================
    # MAIN USER INTERFACE
    # =====================

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.card = QFrame()
        self.card.setObjectName("image_list_card")

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(20, 20, 20, 18)
        card_layout.setSpacing(14)

        # =====================
        # HEADER
        # =====================

        header = QHBoxLayout()
        header.setSpacing(12)

        header_text = QVBoxLayout()
        header_text.setSpacing(6)

        eyebrow = QLabel("IMAGE WORKSPACE")
        eyebrow.setObjectName("image_list_eyebrow")

        title = QLabel("Image Collection")
        title.setObjectName("image_list_title")

        description = QLabel("Manage images added to your processing queue.")
        description.setObjectName("image_list_description")
        description.setWordWrap(True)

        header_text.addWidget(eyebrow)
        header_text.addWidget(title)
        header_text.addWidget(description)

        self.count_label = QLabel("0 IMAGES")
        self.count_label.setObjectName("image_list_count")
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header.addLayout(header_text, 1)
        header.addWidget(self.count_label, 0, Qt.AlignmentFlag.AlignTop)
        card_layout.addLayout(header)

        # =====================
        # VIRTUAL GRID LIST
        # =====================

        self.list = QListWidget()
        self.list.setObjectName("image_list_scroll")
        self.list.viewport().installEventFilter(self)
        self.list.setFrameShape(QFrame.Shape.NoFrame)
        self.list.setFixedHeight(236)
        self.list.setViewMode(QListView.ViewMode.IconMode)
        self.list.setMovement(QListView.Movement.Static)
        self.list.setResizeMode(QListView.ResizeMode.Adjust)
        self.list.setFlow(QListView.Flow.LeftToRight)
        self.list.setWrapping(True)
        self.update_grid_size()
        self.list.setUniformItemSizes(True)
        self.list.setWordWrap(False)
        self.list.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.list.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.list.setMouseTracking(True)
        self.list.setItemDelegate(ImageTileDelegate(self))
        self.list.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        self.list.itemClicked.connect(self.on_item_clicked)

        card_layout.addWidget(self.list, 1)

        # =====================
        # EMPTY STATE
        # =====================

        self.empty_state = self.create_empty_state()
        card_layout.addWidget(self.empty_state)

        # =====================
        # SELECTION STATUS
        # =====================

        selection_layout = QHBoxLayout()
        selection_layout.setSpacing(8)

        selection_icon = QLabel(SELECTION_GLYPH)
        selection_icon.setObjectName("image_list_selection_icon")

        self.selection_label = QLabel("Select an image to inspect or remove it.")
        self.selection_label.setObjectName("image_list_selection_text")
        self.selection_label.setWordWrap(True)

        selection_layout.addWidget(selection_icon)
        selection_layout.addWidget(self.selection_label, 1)
        card_layout.addLayout(selection_layout)

        # =====================
        # BUTTON BAR
        # =====================

        self.button_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.button_layout.setSpacing(10)

        self.sort_button = QPushButton(f"{SORT_GLYPH}  Sort Images")
        self.sort_button.setObjectName("image_list_sort_button")
        self.sort_button.setMinimumHeight(40)
        self.sort_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sort_button.clicked.connect(self.show_sort_menu)

        self.remove_button = QPushButton(f"{REMOVE_GLYPH}  Remove Selected")
        self.remove_button.setObjectName("image_list_remove_button")
        self.remove_button.setMinimumHeight(40)
        self.remove_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.remove_button.clicked.connect(self.remove_selected)

        self.delete_all_button = QPushButton("Clear List")
        self.delete_all_button.setObjectName("image_list_clear_button")
        self.delete_all_button.setMinimumHeight(40)
        self.delete_all_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_all_button.clicked.connect(self.delete_all)

        self.button_layout.addWidget(self.sort_button, 1)
        self.button_layout.addWidget(self.remove_button, 1)
        self.button_layout.addWidget(self.delete_all_button, 1)
        card_layout.addLayout(self.button_layout)

        main_layout.addWidget(self.card)

    # =====================
    # EMPTY STATE
    # =====================

    def create_empty_state(self):
        frame = QFrame()
        frame.setObjectName("image_list_empty_state")
        frame.setFixedHeight(236)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(18, 20, 18, 20)
        layout.setSpacing(9)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = QLabel("\u25a7")
        icon.setObjectName("image_list_empty_icon")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("No Images Added")
        title.setObjectName("image_list_empty_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Import images using the drop area to see them here.")
        subtitle.setObjectName("image_list_empty_description")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)

        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        return frame

    # =====================
    # SET IMAGE COLLECTION
    # =====================

    def set_images(self, images):
        self.images = [Path(image) for image in images]
        self.selected_index = None
        self.selected_image = None
        self.refresh()

    # =====================
    # REFRESH IMAGE GRID
    # =====================

    def refresh(self):
        previous_selection = self.selected_image

        self.list.setUpdatesEnabled(False)
        self.list.clear()
        self.selected_index = None
        self.selected_image = None

        for index, image in enumerate(self.images):
            item = QListWidgetItem()
            item.setToolTip(str(image))
            item.setData(
                Qt.ItemDataRole.AccessibleTextRole, f"Select image: {image.name}"
            )
            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            self.list.addItem(item)

        self.list.setUpdatesEnabled(True)
        self.list.viewport().update()
        self.update_count()
        self.update_empty_state()
        self.update_grid_size()

        if previous_selection is not None and previous_selection in self.images:
            self.select_image(
                self.images.index(previous_selection),
                emit_signal=False,
            )

        self.update_action_states()
        self.images_changed.emit(self.images.copy())

    # =====================
    # IMAGE SELECTION
    # =====================

    def on_item_clicked(self, item):
        row = self.list.row(item)
        if 0 <= row < len(self.images):
            self.select_image(row)

    def select_image(self, index, emit_signal=True):
        if not (0 <= index < len(self.images)):
            return

        self.selected_index = index
        self.selected_image = self.images[index]
        self.list.setCurrentRow(index)
        self.list.viewport().update()
        self.update_action_states()

        if emit_signal:
            self.image_selected.emit(self.selected_image)

    # =====================
    # EMPTY STATE TOGGLE
    # =====================

    def update_empty_state(self):
        has_images = bool(self.images)
        self.list.setVisible(has_images)
        self.empty_state.setVisible(not has_images)

    # =====================
    # UPDATE IMAGE COUNT
    # =====================

    def update_count(self):
        count = len(self.images)
        if count == 1:
            self.count_label.setText("1 IMAGE")
        else:
            self.count_label.setText(f"{count} IMAGES")

    # =====================
    # UPDATE BUTTON STATES
    # =====================

    def update_action_states(self):
        has_images = bool(self.images)
        has_selection = self.selected_index is not None

        self.sort_button.setEnabled(len(self.images) > 1)
        self.remove_button.setEnabled(has_selection)
        self.delete_all_button.setEnabled(has_images)

        if has_selection and self.selected_image is not None:
            filename = self.selected_image.name
            self.selection_label.setText(f"Selected: {filename}")
            self.selection_label.setToolTip(str(self.selected_image))
        elif has_images:
            self.selection_label.setText(
                "Select an image to inspect or remove it."
            )
            self.selection_label.setToolTip("")
        else:
            self.selection_label.setText("Your image collection is empty.")
            self.selection_label.setToolTip("")

    # =====================
    # REMOVE / CLEAR
    # =====================

    def remove_selected(self):
        if self.selected_index is None:
            return
        if not (0 <= self.selected_index < len(self.images)):
            return

        del self.images[self.selected_index]
        self.selected_index = None
        self.selected_image = None
        self.refresh()

    def delete_all(self):
        if not self.images:
            return
        self.images.clear()
        self.selected_index = None
        self.selected_image = None
        self.refresh()

    # =====================
    # SORT
    # =====================

    def show_sort_menu(self):
        if len(self.images) < 2:
            return

        menu = QMenu(self)
        menu.setObjectName("image_list_sort_menu")
        asc_action = menu.addAction("\u2191  Name: A to Z")
        desc_action = menu.addAction("\u2193  Name: Z to A")
        action = menu.exec(
            self.sort_button.mapToGlobal(self.sort_button.rect().bottomLeft())
        )

        if action == asc_action:
            self.sort_ascending_names()
        elif action == desc_action:
            self.sort_descending_names()

    def sort_ascending_names(self):
        self.images.sort(key=lambda path: (path.name.casefold(), str(path).casefold()))
        self.refresh()

    def sort_descending_names(self):
        self.images.sort(
            key=lambda path: (path.name.casefold(), str(path).casefold()),
            reverse=True,
        )
        self.refresh()

    # =====================
    # GET IMAGES
    # =====================

    def get_images(self):
        return self.images.copy()

    # =====================
    # RESPONSIVE ACTION BAR
    # =====================

    def showEvent(self, event):
        super().showEvent(event)
        self.update_grid_size()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.update_grid_size()

        if not hasattr(self, "button_layout"):
            return

        if self.width() < 470:
            self.button_layout.setDirection(QBoxLayout.Direction.TopToBottom)
        else:
            self.button_layout.setDirection(QBoxLayout.Direction.LeftToRight)

    def eventFilter(self, watched, event):
        # The list's own resize event fires before its viewport has been
        # resized, so re-run the grid computation once the viewport reports
        # its final dimensions.
        if watched is self.list.viewport() and event.type() == QEvent.Type.Resize:
            self._grid_timer.start()

        return super().eventFilter(watched, event)

    # =====================
    # STYLING
    # =====================

    def apply_styles(self):
        apply_image_list_style(self)
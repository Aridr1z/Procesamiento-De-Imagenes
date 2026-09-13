from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QBrush, QColor, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (
    QGraphicsEllipseItem,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsSimpleTextItem,
    QGraphicsView,
)

COLOR_PUNTO_A = QColor(220, 30, 30)
COLOR_PUNTO_B = QColor(30, 140, 230)


class ImageView(QGraphicsView):
    """Widget con zoom y pan para mostrar una imagen (QPixmap)."""

    point_a_selected = Signal(tuple)
    points_selected = Signal(tuple, tuple)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self._pixmap_item = QGraphicsPixmapItem()
        self._scene.addItem(self._pixmap_item)

        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setBackgroundBrush(Qt.GlobalColor.darkGray)

        self._picking_active = False
        self._punto_a: tuple[int, int] | None = None
        self._marcadores: list = []

    def set_pixmap(self, pixmap: QPixmap) -> None:
        self._pixmap_item.setPixmap(pixmap)
        self._scene.setSceneRect(self._pixmap_item.boundingRect())
        self._limpiar_marcadores()
        self.fit_to_window()

    def has_image(self) -> bool:
        return not self._pixmap_item.pixmap().isNull()

    def pixmap(self) -> QPixmap:
        return self._pixmap_item.pixmap()

    def fit_to_window(self) -> None:
        if self.has_image():
            self.fitInView(self._pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)

    def zoom_in(self) -> None:
        self.scale(1.25, 1.25)

    def zoom_out(self) -> None:
        self.scale(0.8, 0.8)

    def actual_size(self) -> None:
        self.resetTransform()

    def start_point_picking(self) -> None:
        if not self.has_image():
            return
        self._limpiar_marcadores()
        self._punto_a = None
        self._picking_active = True
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setCursor(Qt.CursorShape.CrossCursor)

    def _limpiar_marcadores(self) -> None:
        for item in self._marcadores:
            self._scene.removeItem(item)
        self._marcadores.clear()

    def _agregar_marcador(self, punto: tuple[int, int], color: QColor, etiqueta: str) -> None:
        pixmap = self._pixmap_item.pixmap()
        radio = max(4, min(pixmap.width(), pixmap.height()) // 150)
        x, y = punto

        circulo = QGraphicsEllipseItem(x - radio, y - radio, radio * 2, radio * 2)
        circulo.setBrush(QBrush(color))
        circulo.setPen(QPen(Qt.GlobalColor.white, 1))
        self._scene.addItem(circulo)
        self._marcadores.append(circulo)

        texto = QGraphicsSimpleTextItem(etiqueta)
        texto.setBrush(QBrush(color))
        texto.setPos(x + radio, y - radio - 14)
        self._scene.addItem(texto)
        self._marcadores.append(texto)

    def _punto_desde_evento(self, event) -> tuple[int, int] | None:
        pixmap = self._pixmap_item.pixmap()
        if pixmap.isNull():
            return None
        punto_escena = self.mapToScene(event.position().toPoint())
        x = min(max(int(punto_escena.x()), 0), pixmap.width() - 1)
        y = min(max(int(punto_escena.y()), 0), pixmap.height() - 1)
        return (x, y)

    def mousePressEvent(self, event) -> None:
        if not self._picking_active:
            super().mousePressEvent(event)
            return

        punto = self._punto_desde_evento(event)
        if punto is None:
            return

        if self._punto_a is None:
            self._punto_a = punto
            self._agregar_marcador(punto, COLOR_PUNTO_A, "A")
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self.point_a_selected.emit(punto)
            return

        self._agregar_marcador(punto, COLOR_PUNTO_B, "B")
        self._picking_active = False
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.unsetCursor()
        punto_a, self._punto_a = self._punto_a, None
        self.points_selected.emit(punto_a, punto)

    def wheelEvent(self, event) -> None:
        if not self.has_image():
            super().wheelEvent(event)
            return
        factor = 1.25 if event.angleDelta().y() > 0 else 0.8
        self.scale(factor, factor)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.fit_to_window()

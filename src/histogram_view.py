from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget

from src.processing.histogram import Histograma


class HistogramView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(320, 200)
        self._rojo: Histograma = [0] * 256
        self._verde: Histograma = [0] * 256
        self._azul: Histograma = [0] * 256

    def set_histogramas(self, rojo: Histograma, verde: Histograma, azul: Histograma) -> None:
        self._rojo = rojo
        self._verde = verde
        self._azul = azul
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), Qt.GlobalColor.white)

        maximo = max(max(self._rojo), max(self._verde), max(self._azul), 1)
        ancho = self.width()
        alto = self.height()
        paso = ancho / 255

        for datos, color in (
            (self._rojo, QColor(220, 60, 60)),
            (self._verde, QColor(60, 170, 90)),
            (self._azul, QColor(60, 110, 220)),
        ):
            painter.setPen(QPen(color, 1))
            puntos = [
                (x * paso, alto - (valor / maximo) * alto)
                for x, valor in enumerate(datos)
            ]
            for (x1, y1), (x2, y2) in zip(puntos, puntos[1:]):
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))

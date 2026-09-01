from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QVBoxLayout

from src.histogram_view import HistogramView
from src.processing.histogram import calcular_histograma


class HistogramDialog(QDialog):
    def __init__(self, pixmap: QPixmap, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Histograma")
        self.resize(500, 300)

        rojo, verde, azul = calcular_histograma(pixmap)

        vista = HistogramView(self)
        vista.set_histogramas(rojo, verde, azul)

        layout = QVBoxLayout(self)
        layout.addWidget(vista)

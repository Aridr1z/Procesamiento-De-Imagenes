from dataclasses import dataclass
from typing import Callable

from PySide6.QtGui import QImage, QPixmap

FilterFunc = Callable[[QPixmap], QPixmap]


@dataclass(frozen=True)
class Filter:
    name: str
    apply: FilterFunc


def escala_de_grises(pixmap: QPixmap) -> QPixmap:
    imagen = pixmap.toImage().convertToFormat(QImage.Format.Format_RGB32)
    ancho = imagen.width()
    alto = imagen.height()

    for y in range(alto):
        fila = imagen.scanLine(y)
        for x in range(ancho):
            i = x * 4
            azul, verde, rojo = fila[i], fila[i + 1], fila[i + 2]
            gris = round(0.299 * rojo + 0.587 * verde + 0.114 * azul)
            fila[i] = fila[i + 1] = fila[i + 2] = gris

    return QPixmap.fromImage(imagen)

def escala_normal(pixmap: QPixmap) -> QPixmap:
    imagen = pixmap.toImage().convertToFormat(QImage.Format.Format_RGB32)
    ancho = imagen.width()
    alto = imagen.height()

    for y in range(alto):
        fila = imagen.scanLine(y)
        for x in range(ancho):
            j = x * 4
            azul, verde, rojo = fila[j], fila[j + 1], fila[j + 2]
            gris = round(0.800 * rojo + 0.887 * verde + 0.814 * azul)
            fila[j] = fila[j + 1] = fila[j + 2] = gris

    return QPixmap.fromImage(imagen)




FILTERS: list[Filter] = [
    Filter("Escala de grises", escala_de_grises),
    Filter("Escala normal", escala_normal),
]

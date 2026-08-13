from dataclasses import dataclass
from typing import Callable

from PySide6.QtGui import QImage, QPixmap

FilterFunc = Callable[[QPixmap], QPixmap]


@dataclass(frozen=True)
class Filter:
    name: str
    apply: FilterFunc


def escala_de_grises(pixmap: QPixmap) -> QPixmap:
    imagen_gris = pixmap.toImage().convertToFormat(QImage.Format.Format_Grayscale8)
    return QPixmap.fromImage(imagen_gris)


FILTERS: list[Filter] = [
    Filter("Escala de grises", escala_de_grises),
]

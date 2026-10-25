from dataclasses import dataclass
from typing import Callable

from PySide6.QtGui import QImage, QPixmap

from src.processing.box import filtro_box
from src.processing.color_math import luminancia_relativa_pixel
from src.processing.suavizado import KERNEL_SUAVIZADO_3X3, Matriz, convolucionar

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


def luminancia_relativa(pixmap: QPixmap) -> QPixmap:
    imagen = pixmap.toImage().convertToFormat(QImage.Format.Format_RGB32)
    ancho = imagen.width()
    alto = imagen.height()

    for y in range(alto):
        fila = imagen.scanLine(y)
        for x in range(ancho):
            i = x * 4
            azul, verde, rojo = fila[i], fila[i + 1], fila[i + 2]
            gris = luminancia_relativa_pixel(rojo, verde, azul)
            fila[i] = fila[i + 1] = fila[i + 2] = gris

    return QPixmap.fromImage(imagen)


def _aplicar_por_canal(
    pixmap: QPixmap, operacion: Callable[[Matriz], Matriz]
) -> QPixmap:
    imagen = pixmap.toImage().convertToFormat(QImage.Format.Format_RGB32)
    ancho = imagen.width()
    alto = imagen.height()

    canales: list[Matriz] = [[], [], []]
    for y in range(alto):
        fila = imagen.scanLine(y)
        for c in range(3):
            canales[c].append([float(fila[x * 4 + c]) for x in range(ancho)])

    procesados = [operacion(canal) for canal in canales]

    for y in range(alto):
        fila = imagen.scanLine(y)
        for c in range(3):
            fila_procesada = procesados[c][y]
            for x in range(ancho):
                fila[x * 4 + c] = min(max(round(fila_procesada[x]), 0), 255)

    return QPixmap.fromImage(imagen)


def suavizado(pixmap: QPixmap) -> QPixmap:
    return _aplicar_por_canal(
        pixmap, lambda canal: convolucionar(canal, KERNEL_SUAVIZADO_3X3)
    )


def box(pixmap: QPixmap, tamano: int) -> QPixmap:
    return _aplicar_por_canal(pixmap, lambda canal: filtro_box(canal, tamano))


FILTERS: list[Filter] = [
    Filter("Escala de grises", escala_de_grises),
    Filter("Luminancia relativa", luminancia_relativa),
    Filter("Suavizado (promedio 3x3)", suavizado),
]

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


def _srgb_a_lineal(valor: int) -> float:
    normalizado = valor / 255
    if normalizado <= 0.03928:
        return normalizado / 12.92
    return ((normalizado + 0.055) / 1.055) ** 2.4


def _lineal_a_srgb(valor: float) -> int:
    if valor <= 0.0031308:
        srgb = valor * 12.92
    else:
        srgb = 1.055 * valor ** (1 / 2.4) - 0.055
    return round(min(max(srgb, 0.0), 1.0) * 255)


_LUT_SRGB_A_LINEAL = [_srgb_a_lineal(v) for v in range(256)]


def luminancia_relativa_pixel(rojo: int, verde: int, azul: int) -> int:
    luminancia = (
        0.2126 * _LUT_SRGB_A_LINEAL[rojo]
        + 0.7152 * _LUT_SRGB_A_LINEAL[verde]
        + 0.0722 * _LUT_SRGB_A_LINEAL[azul]
    )
    return _lineal_a_srgb(luminancia)


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


FILTERS: list[Filter] = [
    Filter("Escala de grises", escala_de_grises),
    Filter("Escala normal", escala_normal),
    Filter("Luminancia relativa", luminancia_relativa),
]

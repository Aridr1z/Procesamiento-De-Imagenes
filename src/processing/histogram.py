from PySide6.QtGui import QImage, QPixmap

Histograma = list[int]


def calcular_histograma(pixmap: QPixmap) -> tuple[Histograma, Histograma, Histograma]:
    imagen = pixmap.toImage().convertToFormat(QImage.Format.Format_RGB32)
    ancho = imagen.width()
    alto = imagen.height()

    rojo: Histograma = [0] * 256
    verde: Histograma = [0] * 256
    azul: Histograma = [0] * 256

    for y in range(alto):
        fila = imagen.scanLine(y)
        for x in range(ancho):
            i = x * 4
            azul[fila[i]] += 1
            verde[fila[i + 1]] += 1
            rojo[fila[i + 2]] += 1

    return rojo, verde, azul

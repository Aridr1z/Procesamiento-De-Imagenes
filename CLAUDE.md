# Procesamiento de Imagenes

Proyecto de Python para procesamiento de imagenes. Etapa actual: visor de
imagenes de escritorio con filtros basicos de color y calculo/visualizacion
de histograma (base sobre la que se agregaran mas operaciones de
procesamiento: transformaciones geometricas, ecualizacion, etc.).

## Stack

- Python 3 (venv en `.venv/`)
- PySide6 (Qt for Python) para la interfaz de escritorio
- `QGraphicsView`/`QGraphicsScene` para el render de la imagen (zoom con
  rueda del mouse, pan con drag, ajustar a ventana)
- Procesamiento en Python puro (sin numpy/opencv), iterando sobre
  `QImage.scanLine` en formato `Format_RGB32` (orden de bytes BGRA)

## Estructura

```
main.py                    # punto de entrada, arranca QApplication + MainWindow
src/
  main_window.py            # QMainWindow: menu, toolbar, abrir archivo, histograma
  image_view.py              # widget de visualizacion (zoom/pan) de un QPixmap
  filters_panel.py           # panel lateral: botones de filtros + calculadora RGB
  histogram_dialog.py        # dialogo que muestra el histograma de la imagen actual
  histogram_view.py          # widget que dibuja el histograma (curvas R/G/B)
  processing/
    filters.py                # filtros sobre QPixmap (escala de grises, etc.)
    color_math.py              # conversion sRGB<->lineal, luminancia relativa
    histogram.py                # calculo de histograma (conteos por canal 0-255)
    distancias.py                # distancias euclidiana, city block, chessboard
    suavizado.py                 # convolucion generica + kernel promedio 3x3
    box.py                       # filtro Box NxN (promedio separable, suma deslizante)
    gauss.py                     # filtro Gaussiano NxN con sigma (kernel separable)
    laplace.py                   # Laplaciano 4/8 vecinos: bordes y realce
requirements.txt
```

## Como correr

```bash
source .venv/bin/activate
pip install -r requirements.txt   # solo la primera vez o si cambian deps
python main.py
```

## Convenciones

- Todo el codigo de la app vive bajo `src/`; `main.py` solo arma y lanza la
  `QApplication`.
- Los widgets de UI son responsables solo de la interfaz; la logica de
  procesamiento de imagenes (cuando se agregue) deberia vivir en modulos
  separados (p. ej. `src/processing/`) y ser invocada desde la UI, no mezclada
  con el codigo de Qt.
- Sin comentarios explicativos de "que hace" el codigo; los nombres deben ser
  suficientemente claros.

## Proximos pasos esperados (no implementados aun)

- Ecualizacion de histograma (distinta del histograma ya implementado, que
  solo calcula/muestra la distribucion de intensidades).
- Transformaciones geometricas.
- Panel para aplicar/comparar operaciones sobre la imagen cargada.

No agregar `numpy`/`opencv-python` ni otras dependencias/funcionalidades
hasta que se pidan explicitamente; se documentan aca solo como contexto de
hacia donde va el proyecto.

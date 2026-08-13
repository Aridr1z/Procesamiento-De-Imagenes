# Procesamiento de Imagenes

Proyecto de Python para procesamiento de imagenes. Etapa actual: visor de
imagenes de escritorio (base sobre la que se agregaran operaciones de
procesamiento mas adelante: filtros, transformaciones, analisis, etc.).

## Stack

- Python 3 (venv en `.venv/`)
- PySide6 (Qt for Python) para la interfaz de escritorio
- `QGraphicsView`/`QGraphicsScene` para el render de la imagen (zoom con
  rueda del mouse, pan con drag, ajustar a ventana)

## Estructura

```
main.py               # punto de entrada, arranca QApplication + MainWindow
src/
  main_window.py       # QMainWindow: menu, toolbar, dialogo de abrir archivo
  image_view.py         # widget de visualizacion (zoom/pan) de un QPixmap
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

- Operaciones de procesamiento (escala de grises, filtros, transformaciones
  geometricas, histogramas, etc.), probablemente con `numpy`/`opencv-python`.
- Panel para aplicar/comparar operaciones sobre la imagen cargada.

No agregar estas dependencias ni funcionalidades hasta que se pidan
explicitamente; se documentan aca solo como contexto de hacia donde va el
proyecto.

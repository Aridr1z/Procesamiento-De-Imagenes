# Procesamiento de Imagenes

Proyecto en Python para procesamiento de imagenes. Por ahora incluye un
visor de imagenes de escritorio (PySide6/Qt) con zoom y pan, base sobre la
que se iran agregando operaciones de procesamiento.

## Requisitos

- Python 3.10+

## Instalacion y ejecucion

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Desde la app: `Archivo > Abrir...` (o `Cmd/Ctrl+O`) para cargar una imagen.
Rueda del mouse para zoom, arrastrar para pan, `Ver > Ajustar a ventana`
para reencuadrar.

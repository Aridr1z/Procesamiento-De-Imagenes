from pathlib import Path

from PySide6.QtGui import QAction, QImageReader, QKeySequence, QPixmap
from PySide6.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QSplitter, QToolBar

from src.filters_panel import FiltersPanel
from src.image_view import ImageView
from src.processing.filters import Filter


def _supported_extensions_filter() -> str:
    formats = [fmt.data().decode() for fmt in QImageReader.supportedImageFormats()]
    return " ".join(f"*.{fmt}" for fmt in formats)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualizador de Imagenes")
        self.resize(1000, 700)

        self.image_view = ImageView(self)
        self.filters_panel = FiltersPanel(self)
        self.filters_panel.filter_selected.connect(self.apply_filter)

        splitter = QSplitter(self)
        splitter.addWidget(self.image_view)
        splitter.addWidget(self.filters_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)
        self.setCentralWidget(splitter)

        self._current_path: Path | None = None
        self._original_pixmap: QPixmap | None = None

        self._build_actions()
        self._build_toolbar()
        self._build_menu()
        self.statusBar().showMessage("Listo")

    def _build_actions(self) -> None:
        self.open_action = QAction("&Abrir...", self)
        self.open_action.setShortcut(QKeySequence.StandardKey.Open)
        self.open_action.triggered.connect(self.open_image)

        self.zoom_in_action = QAction("Acercar", self)
        self.zoom_in_action.setShortcut(QKeySequence.StandardKey.ZoomIn)
        self.zoom_in_action.triggered.connect(self.image_view.zoom_in)

        self.zoom_out_action = QAction("Alejar", self)
        self.zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut)
        self.zoom_out_action.triggered.connect(self.image_view.zoom_out)

        self.fit_action = QAction("Ajustar a ventana", self)
        self.fit_action.triggered.connect(self.image_view.fit_to_window)

        self.actual_size_action = QAction("Tamano real", self)
        self.actual_size_action.triggered.connect(self.image_view.actual_size)

        self.reset_action = QAction("Restablecer imagen", self)
        self.reset_action.triggered.connect(self.reset_image)

        self.exit_action = QAction("&Salir", self)
        self.exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        self.exit_action.triggered.connect(self.close)

    def _build_toolbar(self) -> None:
        toolbar = QToolBar("Principal", self)
        toolbar.addAction(self.open_action)
        toolbar.addSeparator()
        toolbar.addAction(self.zoom_in_action)
        toolbar.addAction(self.zoom_out_action)
        toolbar.addAction(self.fit_action)
        toolbar.addAction(self.actual_size_action)
        toolbar.addSeparator()
        toolbar.addAction(self.reset_action)
        self.addToolBar(toolbar)

    def _build_menu(self) -> None:
        file_menu = self.menuBar().addMenu("&Archivo")
        file_menu.addAction(self.open_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        view_menu = self.menuBar().addMenu("&Ver")
        view_menu.addAction(self.zoom_in_action)
        view_menu.addAction(self.zoom_out_action)
        view_menu.addAction(self.fit_action)
        view_menu.addAction(self.actual_size_action)
        view_menu.addSeparator()
        view_menu.addAction(self.reset_action)

    def open_image(self) -> None:
        path_str, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir imagen",
            "",
            f"Imagenes ({_supported_extensions_filter()})",
        )
        if not path_str:
            return
        self.load_image(Path(path_str))

    def load_image(self, path: Path) -> None:
        pixmap = QPixmap(str(path))
        if pixmap.isNull():
            QMessageBox.warning(self, "Error", f"No se pudo abrir la imagen:\n{path}")
            return

        self._current_path = path
        self._original_pixmap = pixmap
        self.image_view.set_pixmap(pixmap)
        self.setWindowTitle(f"Visualizador de Imagenes - {path.name}")
        self.statusBar().showMessage(
            f"{path.name}  |  {pixmap.width()} x {pixmap.height()} px"
        )

    def apply_filter(self, filter_: Filter) -> None:
        if not self.image_view.has_image():
            return
        self.image_view.set_pixmap(filter_.apply(self.image_view.pixmap()))

    def reset_image(self) -> None:
        if self._original_pixmap is None:
            return
        self.image_view.set_pixmap(self._original_pixmap)

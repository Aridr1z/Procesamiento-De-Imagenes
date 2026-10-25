from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from src.processing.color_math import luminancia_relativa_pixel
from src.processing.filters import FILTERS, MODOS_LAPLACE, Filter
from src.processing.laplace import KERNELS_LAPLACE


class FiltersPanel(QWidget):
    filter_selected = Signal(Filter)
    points_mode_requested = Signal()
    box_filter_requested = Signal(int)
    gauss_filter_requested = Signal(int, float)
    laplace_filter_requested = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(180)
        self.setMaximumWidth(260)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(8, 8, 8, 8)
        self._layout.setSpacing(6)

        self._layout.addWidget(QLabel("Filtros"))
        self._build_buttons()
        self._build_box_filter()
        self._build_gauss_filter()
        self._build_laplace_filter()
        self._layout.addStretch()
        self._build_puntos_calculator()
        self._build_rgb_calculator()

    def _build_buttons(self) -> None:
        if not FILTERS:
            placeholder = QLabel("(sin filtros aun)")
            placeholder.setEnabled(False)
            self._layout.addWidget(placeholder)
            return

        for filter_ in FILTERS:
            button = QPushButton(filter_.name, self)
            button.clicked.connect(
                lambda _checked=False, f=filter_: self.filter_selected.emit(f)
            )
            self._layout.addWidget(button)

    def _build_box_filter(self) -> None:
        separador = QFrame(self)
        separador.setFrameShape(QFrame.Shape.HLine)
        self._layout.addWidget(separador)

        self._layout.addWidget(QLabel("Filtro Box"))

        tamano_layout = QHBoxLayout()
        tamano_layout.addWidget(QLabel("Tamano (NxN)"))
        self._tamano_box_spin = QSpinBox(self)
        self._tamano_box_spin.setRange(3, 31)
        self._tamano_box_spin.setSingleStep(2)
        self._tamano_box_spin.setValue(3)
        self._tamano_box_spin.editingFinished.connect(self._forzar_tamano_impar)
        tamano_layout.addWidget(self._tamano_box_spin)
        self._layout.addLayout(tamano_layout)

        boton_box = QPushButton("Aplicar filtro Box", self)
        boton_box.clicked.connect(self._emitir_filtro_box)
        self._layout.addWidget(boton_box)

    def _forzar_tamano_impar(self) -> None:
        valor = self._tamano_box_spin.value()
        if valor % 2 == 0:
            self._tamano_box_spin.setValue(valor + 1)

    def _emitir_filtro_box(self) -> None:
        self._forzar_tamano_impar()
        self.box_filter_requested.emit(self._tamano_box_spin.value())

    def _build_gauss_filter(self) -> None:
        separador = QFrame(self)
        separador.setFrameShape(QFrame.Shape.HLine)
        self._layout.addWidget(separador)

        self._layout.addWidget(QLabel("Filtro Gauss"))

        tamano_layout = QHBoxLayout()
        tamano_layout.addWidget(QLabel("Tamano (NxN)"))
        self._tamano_gauss_spin = QSpinBox(self)
        self._tamano_gauss_spin.setRange(3, 31)
        self._tamano_gauss_spin.setSingleStep(2)
        self._tamano_gauss_spin.setValue(5)
        self._tamano_gauss_spin.editingFinished.connect(self._forzar_tamano_gauss_impar)
        tamano_layout.addWidget(self._tamano_gauss_spin)
        self._layout.addLayout(tamano_layout)

        sigma_layout = QHBoxLayout()
        sigma_layout.addWidget(QLabel("Sigma"))
        self._sigma_gauss_spin = QDoubleSpinBox(self)
        self._sigma_gauss_spin.setRange(0.1, 10.0)
        self._sigma_gauss_spin.setSingleStep(0.1)
        self._sigma_gauss_spin.setDecimals(1)
        self._sigma_gauss_spin.setValue(1.0)
        sigma_layout.addWidget(self._sigma_gauss_spin)
        self._layout.addLayout(sigma_layout)

        boton_gauss = QPushButton("Aplicar filtro Gauss", self)
        boton_gauss.clicked.connect(self._emitir_filtro_gauss)
        self._layout.addWidget(boton_gauss)

    def _forzar_tamano_gauss_impar(self) -> None:
        valor = self._tamano_gauss_spin.value()
        if valor % 2 == 0:
            self._tamano_gauss_spin.setValue(valor + 1)

    def _emitir_filtro_gauss(self) -> None:
        self._forzar_tamano_gauss_impar()
        self.gauss_filter_requested.emit(
            self._tamano_gauss_spin.value(), self._sigma_gauss_spin.value()
        )

    def _build_laplace_filter(self) -> None:
        separador = QFrame(self)
        separador.setFrameShape(QFrame.Shape.HLine)
        self._layout.addWidget(separador)

        self._layout.addWidget(QLabel("Filtro Laplace"))

        vecindad_layout = QHBoxLayout()
        vecindad_layout.addWidget(QLabel("Vecindad"))
        self._vecindad_laplace_combo = QComboBox(self)
        self._vecindad_laplace_combo.addItems(list(KERNELS_LAPLACE))
        vecindad_layout.addWidget(self._vecindad_laplace_combo)
        self._layout.addLayout(vecindad_layout)

        self._modo_laplace_combo = QComboBox(self)
        self._modo_laplace_combo.addItems(list(MODOS_LAPLACE))
        self._layout.addWidget(self._modo_laplace_combo)

        boton_laplace = QPushButton("Aplicar filtro Laplace", self)
        boton_laplace.clicked.connect(self._emitir_filtro_laplace)
        self._layout.addWidget(boton_laplace)

    def _emitir_filtro_laplace(self) -> None:
        self.laplace_filter_requested.emit(
            self._vecindad_laplace_combo.currentText(),
            self._modo_laplace_combo.currentText(),
        )

    def _build_puntos_calculator(self) -> None:
        separador = QFrame(self)
        separador.setFrameShape(QFrame.Shape.HLine)
        self._layout.addWidget(separador)

        self._layout.addWidget(QLabel("Distancia entre dos puntos"))

        self._boton_seleccionar_puntos = QPushButton("Seleccionar puntos en la imagen", self)
        self._boton_seleccionar_puntos.clicked.connect(self.points_mode_requested.emit)
        self._layout.addWidget(self._boton_seleccionar_puntos)

        self._resultado_puntos_label = QLabel("Sin puntos seleccionados")
        self._resultado_puntos_label.setWordWrap(True)
        self._layout.addWidget(self._resultado_puntos_label)

    def iniciar_seleccion_puntos(self) -> None:
        self._boton_seleccionar_puntos.setEnabled(False)
        self._resultado_puntos_label.setText("Haz click en el punto A de la imagen")

    def marcar_punto_a_elegido(self) -> None:
        self._resultado_puntos_label.setText("Haz click en el punto B de la imagen")

    def mostrar_resultado_puntos(
        self, punto_a: tuple, punto_b: tuple, distancias: dict[str, float]
    ) -> None:
        self._boton_seleccionar_puntos.setEnabled(True)
        self._resultado_puntos_label.setText(
            f"Punto A: {punto_a}\n"
            f"Punto B: {punto_b}\n\n"
            f"Euclidiana: {distancias['euclidiana']:.2f} px\n"
            f"City block: {distancias['city_block']:.2f} px (movimientos ortogonales)\n"
            f"Chessboard: {distancias['chessboard']:.2f} (movimientos tipo rey)"
        )

    def _build_rgb_calculator(self) -> None:
        separador = QFrame(self)
        separador.setFrameShape(QFrame.Shape.HLine)
        self._layout.addWidget(separador)

        self._layout.addWidget(QLabel("Luminancia de un color"))

        entradas_layout = QHBoxLayout()
        self._rojo_spin = QSpinBox(self)
        self._verde_spin = QSpinBox(self)
        self._azul_spin = QSpinBox(self)
        for etiqueta, spin in (
            ("R", self._rojo_spin),
            ("G", self._verde_spin),
            ("B", self._azul_spin),
        ):
            spin.setRange(0, 255)
            spin.valueChanged.connect(self._actualizar_resultado_rgb)
            entradas_layout.addWidget(QLabel(etiqueta))
            entradas_layout.addWidget(spin)
        self._layout.addLayout(entradas_layout)

        self._resultado_rgb_label = QLabel()
        self._layout.addWidget(self._resultado_rgb_label)
        self._actualizar_resultado_rgb()

    def _actualizar_resultado_rgb(self) -> None:
        gris = luminancia_relativa_pixel(
            self._rojo_spin.value(),
            self._verde_spin.value(),
            self._azul_spin.value(),
        )
        self._resultado_rgb_label.setText(f"RGB resultante: {gris}, {gris}, {gris}")

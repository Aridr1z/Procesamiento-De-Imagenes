from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from src.processing.filters import FILTERS, Filter


class FiltersPanel(QWidget):
    filter_selected = Signal(Filter)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(180)
        self.setMaximumWidth(260)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(8, 8, 8, 8)
        self._layout.setSpacing(6)

        self._layout.addWidget(QLabel("Filtros"))
        self._build_buttons()
        self._layout.addStretch()

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

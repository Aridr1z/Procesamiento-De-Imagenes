from dataclasses import dataclass
from typing import Callable

from PySide6.QtGui import QPixmap

FilterFunc = Callable[[QPixmap], QPixmap]


@dataclass(frozen=True)
class Filter:
    name: str
    apply: FilterFunc


FILTERS: list[Filter] = []

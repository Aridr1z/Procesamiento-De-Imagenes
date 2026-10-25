import math

from src.processing.suavizado import Matriz


def kernel_gauss_1d(tamano: int, sigma: float) -> list[float]:
    _validar_parametros(tamano, sigma)
    radio = tamano // 2
    pesos = [math.exp(-(i * i) / (2 * sigma * sigma)) for i in range(-radio, radio + 1)]
    total = sum(pesos)
    return [peso / total for peso in pesos]


def kernel_gauss(tamano: int, sigma: float) -> Matriz:
    pesos = kernel_gauss_1d(tamano, sigma)
    return [[py * px for px in pesos] for py in pesos]


def filtro_gauss(matriz: Matriz, tamano: int, sigma: float) -> Matriz:
    pesos = kernel_gauss_1d(tamano, sigma)
    horizontal = [_convolucionar_1d(fila, pesos) for fila in matriz]
    columnas = [list(columna) for columna in zip(*horizontal)]
    vertical = [_convolucionar_1d(columna, pesos) for columna in columnas]
    return [list(fila) for fila in zip(*vertical)]


def _convolucionar_1d(valores: list[float], pesos: list[float]) -> list[float]:
    radio = len(pesos) // 2
    extendidos = [valores[0]] * radio + valores + [valores[-1]] * radio
    return [
        sum(extendidos[i + k] * peso for k, peso in enumerate(pesos))
        for i in range(len(valores))
    ]


def _validar_parametros(tamano: int, sigma: float) -> None:
    if tamano < 1 or tamano % 2 == 0:
        raise ValueError(f"El tamano del kernel Gauss debe ser impar y positivo: {tamano}")
    if sigma <= 0:
        raise ValueError(f"Sigma debe ser positivo: {sigma}")

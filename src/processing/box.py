from src.processing.suavizado import Matriz


def kernel_box(tamano: int) -> Matriz:
    _validar_tamano(tamano)
    peso = 1 / (tamano * tamano)
    return [[peso] * tamano for _ in range(tamano)]


def filtro_box(matriz: Matriz, tamano: int) -> Matriz:
    _validar_tamano(tamano)
    horizontal = [_promedio_deslizante(fila, tamano) for fila in matriz]
    columnas = [list(columna) for columna in zip(*horizontal)]
    vertical = [_promedio_deslizante(columna, tamano) for columna in columnas]
    return [list(fila) for fila in zip(*vertical)]


def _promedio_deslizante(valores: list[float], tamano: int) -> list[float]:
    radio = tamano // 2
    extendidos = [valores[0]] * radio + valores + [valores[-1]] * radio

    suma = sum(extendidos[:tamano])
    promedios = [suma / tamano]
    for i in range(1, len(valores)):
        suma += extendidos[i + tamano - 1] - extendidos[i - 1]
        promedios.append(suma / tamano)
    return promedios


def _validar_tamano(tamano: int) -> None:
    if tamano < 1 or tamano % 2 == 0:
        raise ValueError(f"El tamano del kernel Box debe ser impar y positivo: {tamano}")

from src.processing.suavizado import Matriz, convolucionar

KERNEL_LAPLACE_4_VECINOS: Matriz = [
    [0, 1, 0],
    [1, -4, 1],
    [0, 1, 0],
]

KERNEL_LAPLACE_8_VECINOS: Matriz = [
    [1, 1, 1],
    [1, -8, 1],
    [1, 1, 1],
]

KERNELS_LAPLACE: dict[str, Matriz] = {
    "4 vecinos": KERNEL_LAPLACE_4_VECINOS,
    "8 vecinos": KERNEL_LAPLACE_8_VECINOS,
}


def laplaciano(matriz: Matriz, vecindad: str) -> Matriz:
    return convolucionar(matriz, KERNELS_LAPLACE[vecindad])


def bordes_laplace(matriz: Matriz, vecindad: str) -> Matriz:
    return [[abs(valor) for valor in fila] for fila in laplaciano(matriz, vecindad)]


def realce_laplace(matriz: Matriz, vecindad: str) -> Matriz:
    return [
        [original - valor for original, valor in zip(fila_original, fila_laplace)]
        for fila_original, fila_laplace in zip(matriz, laplaciano(matriz, vecindad))
    ]

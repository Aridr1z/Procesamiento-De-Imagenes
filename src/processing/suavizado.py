Matriz = list[list[float]]

KERNEL_SUAVIZADO_3X3: Matriz = [
    [1 / 9, 1 / 9, 1 / 9],
    [1 / 9, 1 / 9, 1 / 9],
    [1 / 9, 1 / 9, 1 / 9],
]


def convolucionar(matriz: Matriz, kernel: Matriz) -> Matriz:
    filas = len(matriz)
    columnas = len(matriz[0])
    k_filas = len(kernel)
    k_columnas = len(kernel[0])
    offset_fila = k_filas // 2
    offset_columna = k_columnas // 2

    resultado: Matriz = []
    for y in range(filas):
        fila_resultado = []
        for x in range(columnas):
            acumulado = 0.0
            for ky in range(k_filas):
                for kx in range(k_columnas):
                    fy = min(max(y + ky - offset_fila, 0), filas - 1)
                    fx = min(max(x + kx - offset_columna, 0), columnas - 1)
                    acumulado += matriz[fy][fx] * kernel[ky][kx]
            fila_resultado.append(acumulado)
        resultado.append(fila_resultado)

    return resultado

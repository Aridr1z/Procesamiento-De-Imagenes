import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.processing.suavizado import KERNEL_SUAVIZADO_3X3, Matriz, convolucionar


def es_numero(valor: str) -> bool:
    try:
        float(valor)
        return True
    except ValueError:
        return False


def pedir_entero(mensaje: str, minimo: int = 1) -> int:
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit() and int(valor) >= minimo:
            return int(valor)
        print(f"Valor invalido, ingresa un entero mayor o igual a {minimo}.")


def pedir_fila(numero_fila: int, columnas: int) -> list[float]:
    while True:
        valor = input(f"Fila {numero_fila} ({columnas} valores separados por coma): ")
        partes = [p.strip() for p in valor.split(",")]
        if len(partes) == columnas and all(es_numero(p) for p in partes):
            return [float(p) for p in partes]
        print(f"Ingresa exactamente {columnas} valores numericos separados por coma.")


def pedir_matriz() -> Matriz:
    filas = pedir_entero("Cantidad de filas: ")
    columnas = pedir_entero("Cantidad de columnas: ")
    return [pedir_fila(y + 1, columnas) for y in range(filas)]


def imprimir_matriz(titulo: str, matriz: Matriz) -> None:
    print(f"\n{titulo}")
    for fila in matriz:
        print("  ".join(f"{v:7.2f}" for v in fila))


def main() -> None:
    print("Suavizado por convolucion con una matriz (kernel) promediadora\n")

    matriz = pedir_matriz()
    imprimir_matriz("Matriz original:", matriz)

    imprimir_matriz("Kernel de suavizado (3x3):", KERNEL_SUAVIZADO_3X3)

    resultado = convolucionar(matriz, KERNEL_SUAVIZADO_3X3)
    imprimir_matriz("Matriz suavizada:", resultado)


if __name__ == "__main__":
    main()

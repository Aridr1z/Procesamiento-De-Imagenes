import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.processing.distancias import (
    distancia_chessboard,
    distancia_city_block,
    distancia_euclidiana,
)


def pedir_punto(nombre: str) -> tuple[float, ...]:
    valor = input(f"Punto {nombre} (componentes separadas por coma, ej: 10,20,30): ")
    return tuple(float(v.strip()) for v in valor.split(","))


def main() -> None:
    if len(sys.argv) > 1:
        partes = sys.argv[1:]
        mitad = len(partes) // 2
        p1 = tuple(float(v) for v in partes[:mitad])
        p2 = tuple(float(v) for v in partes[mitad:])
    else:
        p1 = pedir_punto("A")
        p2 = pedir_punto("B")

    print(f"\nPunto A: {p1}")
    print(f"Punto B: {p2}\n")

    print(f"Distancia Euclidiana = {distancia_euclidiana(p1, p2):.4f}")
    print(f"Distancia City-Block = {distancia_city_block(p1, p2):.4f}")
    print(f"Distancia Chessboard = {distancia_chessboard(p1, p2):.4f}")


if __name__ == "__main__":
    main()

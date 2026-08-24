import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.processing.filters import _lineal_a_srgb, _srgb_a_lineal


def pedir_canal(nombre: str) -> int:
    while True:
        valor = input(f"{nombre} (0-255): ").strip()
        if valor.isdigit() and 0 <= int(valor) <= 255:
            return int(valor)
        print("Valor invalido, ingresa un entero entre 0 y 255.")


def main() -> None:
    if len(sys.argv) == 4:
        rojo, verde, azul = (int(v) for v in sys.argv[1:4])
    else:
        rojo = pedir_canal("R")
        verde = pedir_canal("G")
        azul = pedir_canal("B")

    print(f"\nRGB de entrada: ({rojo}, {verde}, {azul})\n")

    rs, gs, bs = rojo / 255, verde / 255, azul / 255
    print(f"Rs = {rojo}/255 = {rs:.4f}")
    print(f"Gs = {verde}/255 = {gs:.4f}")
    print(f"Bs = {azul}/255 = {bs:.4f}\n")

    rl = _srgb_a_lineal(rojo)
    gl = _srgb_a_lineal(verde)
    bl = _srgb_a_lineal(azul)
    print(f"RL = {rl:.4f}")
    print(f"GL = {gl:.4f}")
    print(f"BL = {bl:.4f}\n")

    r_term = 0.2126 * rl
    g_term = 0.7152 * gl
    b_term = 0.0722 * bl
    print(f"0.2126 * RL = {r_term:.4f}")
    print(f"0.7152 * GL = {g_term:.4f}")
    print(f"0.0722 * BL = {b_term:.4f}\n")

    cs_lineal = r_term + g_term + b_term
    print(f"Cs (lineal) = {cs_lineal:.4f}\n")

    cs_srgb = _lineal_a_srgb(cs_lineal)
    print(f"Cs (0-255) = {cs_srgb}")


if __name__ == "__main__":
    main()

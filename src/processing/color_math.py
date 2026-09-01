def srgb_a_lineal(valor: int) -> float:
    normalizado = valor / 255
    if normalizado <= 0.03928:
        return normalizado / 12.92
    return ((normalizado + 0.055) / 1.055) ** 2.4


def lineal_a_srgb(valor: float) -> int:
    if valor <= 0.0031308:
        srgb = valor * 12.92
    else:
        srgb = 1.055 * valor ** (1 / 2.4) - 0.055
    return round(min(max(srgb, 0.0), 1.0) * 255)


_LUT_SRGB_A_LINEAL = [srgb_a_lineal(v) for v in range(256)]


def luminancia_relativa_pixel(rojo: int, verde: int, azul: int) -> int:
    luminancia = (
        0.2126 * _LUT_SRGB_A_LINEAL[rojo]
        + 0.7152 * _LUT_SRGB_A_LINEAL[verde]
        + 0.0722 * _LUT_SRGB_A_LINEAL[azul]
    )
    return lineal_a_srgb(luminancia)

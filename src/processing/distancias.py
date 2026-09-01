Vector = tuple[float, ...]


def distancia_euclidiana(a: Vector, b: Vector) -> float:
    return sum((ai - bi) ** 2 for ai, bi in zip(a, b)) ** 0.5


def distancia_city_block(a: Vector, b: Vector) -> float:
    return sum(abs(ai - bi) for ai, bi in zip(a, b))


def distancia_chessboard(a: Vector, b: Vector) -> float:
    return max(abs(ai - bi) for ai, bi in zip(a, b))

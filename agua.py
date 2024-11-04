from algoritmo import Newton
import numpy as np


def xy(t):
    x = 2 * t
    y = x**2 - 2 * x
    return np.array([x, y])


def dist_to_lake(xy: np.ndarray):
    x, y = xy[0], xy[1]
    return x**2 + 9 * (y + 3 / 2) - 9


def jacobian(xy):
    x, y = xy[0], xy[1]
    # Jacobiano do sistema de equações
    j = np.array(
        [
            [2 * x, 3 * (9 + (y / 2) ** 3) * (y / 2) ** 2],
            [2 * x - 2, 3 * (9 + (y / 2) ** 3) ** 2 * (3 / 4) * (y / 2) ** 2],
        ]
    )
    return j


def expr(x: np.ndarray) -> np.ndarray:
    return dist_to_lake(x)


if __name__ == "__main__":
    algo = Newton(expr, 10**-3, 10**-3, None, False, None, np.zeros((2)), jacobian)
    algo.run()

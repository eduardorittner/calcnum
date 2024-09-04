from algoritmo import Bissection, FalsePosition
from math import sin


def y(t):
    return 2000 + sin(t) - ((3 * 10**-3) / 2 * (t**2))


def robot_expr(t):
    if t < 500:
        return y(t)
    elif t < 1000:
        return y(t) - 2 * (t - 500)
    else:
        return y(t) - 2 * (1500 - t)


if __name__ == "__main__":
    print("Falsa posição")
    algo = FalsePosition(robot_expr, 10**-3, None, False, None, 0, 1500)
    algo.run()

    print("Bisseção")

    algo = Bissection(robot_expr, 10**-3, None, False, None, 0, 1500)
    algo.run()

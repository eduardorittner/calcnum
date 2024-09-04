from typing import Callable, List
from math import log10, fabs, sin


class Algorithm:
    def __init__(
        self,
        expr: Callable,
        precision: float,
        log: bool,
        max_iters: int | None,
    ):
        self.expr = expr
        self.precision = precision
        self.log = log
        self.n = 0
        self.estimate = 0
        self.error = 0
        self.max_iters = 200 if max_iters is None else max_iters

    def stop(self) -> bool:
        """Critério de parada do algoritmo"""
        return self.error < self.precision

    def iterate_once(self) -> bool:
        """Roda uma única iteração do algoritmo"""
        self.n += 1
        self.error = self.next()
        return not self.stop()

    def next(self) -> float:
        assert False, "next method must be implemented by child classes"

    def run(self):
        while self.iterate_once() and self.n < self.max_iters:
            if self.log:
                print(
                    f"Iteration {self.n}: Estimate {self.estimate}, Error {self.error}"
                )

        if self.n == self.max_iters:
            print(
                f"Stopped iterating at max iterations ({self.max_iters}), is your algorithm correct?"
            )

        else:
            print(f"Estimativa final: {self.estimate}, {self.n-1} iterações")


class Bissection(Algorithm):
    def __init__(
        self,
        expr: Callable,
        precision: float,
        log: bool,
        max_iters: int | None,
        a: float,
        b: float,
    ):
        super().__init__(expr, precision, log, max_iters)
        self.a = a
        self.b = b

    def next(self) -> float:
        self.estimate = (self.a + self.b) / 2

        if self.expr(self.estimate) * self.expr(self.a) < 0:
            self.b = self.estimate
        else:
            self.a = self.estimate

        return fabs(self.a - self.b)


class FalsePosition(Algorithm):
    def __init__(
        self,
        expr: Callable,
        precision: float,
        log: bool,
        max_iters: int | None,
        a: float,
        b: float,
    ):
        super().__init__(expr, precision, log, max_iters)
        self.a = a
        self.b = b

    def next(self) -> float:
        self.estimate = (
            (self.a * self.expr(self.b)) - (self.b * self.expr(self.a))
        ) / (self.expr(self.b) - self.expr(self.a))

        if self.expr(self.estimate) * self.expr(self.a) < 0:
            self.a = self.estimate
        else:
            self.b = self.estimate

        return fabs(self.a - self.b)


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
    algo = FalsePosition(robot_expr, 10**-3, False, None, 0, 1500)
    algo.run()

    print("Bisseção")

    algo = Bissection(robot_expr, 10**-3, False, None, 0, 1500)
    algo.run()

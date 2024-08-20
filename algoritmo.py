from typing import Callable
from math import log10, fabs


class Algorithm:
    def __init__(
        self, expr: Callable, precision: float, log: bool, max_iters: int | None
    ):
        self.expr = expr
        self.precision = precision
        self.log = log
        self.n = 0
        self.estimate = None
        self.error = 0
        self.max_iters = 200 if max_iters is None else max_iters

    def stop(self) -> bool:
        """Critério de parada do algoritmo"""
        return False

    def iterate_once(self) -> bool:
        """Roda uma única iteração do algoritmo"""
        self.n += 1
        self.error = self.next()
        return self.stop()

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

        elif self.log:

            print(
                f"Stopped iterating at {self.n} iterations, with error {self.error} and final estimate = {self.estimate}"
            )


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

    def stop(self) -> bool:
        return self.error > self.precision

    def next(self) -> float:
        self.estimate = (self.a + self.b) / 2

        if self.expr(self.estimate) * self.expr(self.a) < 0:
            self.b = self.estimate
        else:
            self.a = self.estimate

        return fabs(self.a - self.b)


def expr(x):
    return x * log10(x) - 1


if __name__ == "__main__":
    bissection = Bissection(expr, 10**-4, True, 100, 2, 3)

    bissection.run()

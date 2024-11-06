from typing import Callable
from math import e


def fn(n: float) -> float:
    return (0.2 * n) - (4 * (10**-3) * (n**2))


class ExplicitEuler:
    def __init__(self, f: Callable, h: float, iters: int):
        self.f = f
        self.h = h
        self.iters = iters
        self.t: float = 0
        self.n = 1

    def true(self, t: float):
        return 50 * ((e ** (0.2 * t))) / (49 + e ** (0.2 * t))

    def run(self):
        i = 0

        while i < self.iters:
            t, n = self.next()
            print(f"({t}, {n}, {self.true(t)})")
            i += 1

    def next(self) -> tuple[float, float]:
        """Returns the pair (t,n)"""

        self.n = self.n + self.h * self.f(self.n)
        self.t += self.h

        return (self.t, self.n)


class ImplicitEuler:
    def __init__(self, f: Callable, h: float, iters: int):
        self.f = f
        self.h = h
        self.iters = iters
        self.t: float = 0
        self.n = 1

    def true(self, t: float):
        return 50 * ((e ** (0.2 * t))) / (49 + e ** (0.2 * t))

    def run(self):
        i = 0

        while i < self.iters:
            t, n = self.next()
            print(f"({t}, {n}, {self.true(t)})")
            i += 1

    def next(self) -> tuple[float, float]:
        """Returns the pair (t,n)"""

        n = 0
        last_n = 0

        # Método do ponto fixo
        while True:
            n = self.n + self.h * self.f(last_n)
            if abs(n - last_n) < 0.0001:
                break
            else:
                last_n = n

        self.n = n
        self.t += self.h

        return (self.t, self.n)


class CrankNikolson:
    def __init__(self, f: Callable, h: float, iters: int):
        self.f = f
        self.h = h
        self.iters = iters
        self.t = 0
        self.n = 0
        self.imp = ImplicitEuler(f, h, iters)
        self.exp = ExplicitEuler(f, h, iters)

    def true(self, t: float):
        return 50 * ((e ** (0.2 * t))) / (49 + e ** (0.2 * t))

    def run(self):
        i = 0

        while i < self.iters:
            t, n = self.next()
            print(f"({t}, {n}, {self.true(t)})")
            i += 1

    def next(self):
        self.t, n1 = self.imp.next()
        self.t, n2 = self.exp.next()

        self.n = (n1 + n2) / 2

        return self.t, self.n


# Só mudar a classe aqui
algo = ImplicitEuler(fn, 0.5, 48)

algo.run()

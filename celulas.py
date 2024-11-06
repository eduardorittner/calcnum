from typing import Callable
from math import e
import pandas as pd
import matplotlib.pyplot as plt


def fn(n: float) -> float:
    return (0.2 * n) - (4 * (10**-3) * (n**2))


def true(t: float) -> float:
    return 50 * ((e ** (0.2 * t))) / (49 + e ** (0.2 * t))


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
            yield n
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
        self.t: float = 1
        self.n = 1

    def true(self, t: float):
        return 50 * ((e ** (0.2 * t))) / (49 + e ** (0.2 * t))

    def run(self):
        i = 0

        while i < self.iters:
            t, n = self.next()
            yield n
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
            yield n
            i += 1

    def next(self):
        self.t, n1 = self.imp.next()
        self.t, n2 = self.exp.next()

        self.n = (n1 + n2) / 2

        return self.t, self.n


stop = 4
step = 0.05
stop = int(stop / step)

imp = ImplicitEuler(fn, step, stop)
imp = list(imp.run())
exp = ExplicitEuler(fn, step, stop)
exp = list(exp.run())
crank = CrankNikolson(fn, step, stop)
crank = list(crank.run())

time = [(i * step) + step for i in range(0, stop, 1)]
true_values = [true(t) for t in time]


def table(time, ref, exp, imp, crank):
    data = {
        "Tempo": time,
        "Real": true_values,
        "Euler Explícito": exp,
        "Euler Implícito": imp,
        "Crank-Nikolson": crank,
    }

    df = pd.DataFrame(data)

    formatted_df = df.style.format("{:.10f}")  # Format numbers to 2 decimal places

    styled_df = (
        formatted_df.format("{:.0f}", subset=["Tempo"])
        .hide()
        .set_table_styles(
            [
                {
                    "selector": "th.col_heading",
                    "props": "padding-right: 30px; padding-left: 30px;",
                },
                {
                    "selector": "th",
                    "props": "text-align: center; border-bottom: 3px solid white; border-left: 3px solid white; border-right: 3px solid white;",
                },
                {
                    "selector": "td",
                    "props": "text-align: center; border-bottom:3px solid white; border-left: 3px solid white; border-right: 3px solid white;",
                },
            ]
        )
    )
    return styled_df.to_html()


def plot(df):
    plot = df.plot(
        "Tempo", ["Real", "Euler Explícito", "Euler Implícito", "Crank-Nikolson"]
    )
    plt.show()


def convergence(stop, steps):
    for step in steps:
        imp = ImplicitEuler(fn, step, stop)
        imp = list(imp.run())
        exp = ExplicitEuler(fn, step, stop)
        exp = list(exp.run())
        crank = CrankNikolson(fn, step, stop)
        crank = list(crank.run())

        time = [(i * step) + step for i in range(0, stop, 1)]
        true_values = [true(t) for t in time]

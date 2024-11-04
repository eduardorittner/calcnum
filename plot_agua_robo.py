import matplotlib.pyplot as plt
import matplotlib.patches as patch
import numpy as np


def plot_trajectory():

    plt.show()


def plot_water():
    circle = patch.Ellipse((0, -1.5), 6, 2, color="blue", fill=True)
    fix, ax = plt.subplots()
    x = np.arange(-5, 5, 0.01)
    y = x**2 - 2 * x
    ax.plot(x, y, "red")
    ax.add_patch(circle)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    plt.xticks(np.arange(-5, 5, 1))
    plt.yticks(np.arange(-5, 5, 1))
    ax.set_aspect("equal")
    plt.show()


plot_water()

# plot_utils.py
import numpy as np
import matplotlib.pyplot as plt
from fuzzy_logic import sludge_mf, grease_mf, time_mf

def plot_membership_functions():
    x = np.linspace(0, 1, 200)

    fig, ax = plt.subplots(3, 1, figsize=(7, 12))

    for label in ["SD", "MD", "LD"]:
        ax[0].plot(x, [sludge_mf(v)[label] for v in x], label=label)
    ax[0].set_title("Sludge Membership Functions")
    ax[0].legend()

    for label in ["NG", "MG", "LG"]:
        ax[1].plot(x, [grease_mf(v)[label] for v in x], label=label)
    ax[1].set_title("Grease Membership Functions")
    ax[1].legend()

    tv = time_mf()
    ax[2].bar(tv.keys(), tv.values())
    ax[2].set_title("Time Output Membership")

    plt.tight_layout()
    plt.show()


def plot_3d_rules():
    from mpl_toolkits.mplot3d import Axes3D

    x = np.linspace(0, 1, 30)
    y = np.linspace(0, 1, 30)

    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)

    from fuzzy_logic import fuzzy_inference

    for i in range(len(x)):
        for j in range(len(y)):
            Z[i, j], _, _ = fuzzy_inference(x[i], y[j])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, cmap="viridis")
    ax.set_title("Fuzzy Inference Surface")
    ax.set_xlabel("Sludge")
    ax.set_ylabel("Grease")
    ax.set_zlabel("Time")
    plt.show()

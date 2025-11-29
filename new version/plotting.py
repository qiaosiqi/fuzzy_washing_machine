# plotting.py
import numpy as np
import matplotlib.pyplot as plt
from membership import mf_trap, mf_tri
from logic import sludge_mf, grease_mf, time_mf, fuzzy_inference


def plot_input_membership():
    x = np.linspace(0, 1, 200)

    plt.figure(figsize=(8, 5))
    plt.title("Sludge Membership Functions")
    plt.plot(x, [mf_trap(i, 0, 0, 0.2, 0.4) for i in x], label="SD")
    plt.plot(x, [mf_trap(i, 0.2, 0.4, 0.6, 0.8) for i in x], label="MD")
    plt.plot(x, [mf_trap(i, 0.6, 0.8, 1, 1) for i in x], label="LD")
    plt.legend()
    plt.grid()
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.title("Grease Membership Functions")
    plt.plot(x, [mf_trap(i, 0, 0, 0.2, 0.4) for i in x], label="NG")
    plt.plot(x, [mf_trap(i, 0.2, 0.4, 0.6, 0.8) for i in x], label="MG")
    plt.plot(x, [mf_trap(i, 0.6, 0.8, 1, 1) for i in x], label="LG")
    plt.legend()
    plt.grid()
    plt.show()


def plot_output_membership():
    x = np.linspace(0, 1, 200)

    plt.figure(figsize=(8, 5))
    plt.title("Washing Time Membership Functions")
    plt.plot(x, [mf_tri(i, 0, 0, 0.2) for i in x], label="VS")
    plt.plot(x, [mf_tri(i, 0.1, 0.3, 0.5) for i in x], label="S")
    plt.plot(x, [mf_tri(i, 0.3, 0.5, 0.7) for i in x], label="M")
    plt.plot(x, [mf_tri(i, 0.5, 0.7, 0.9) for i in x], label="L")
    plt.plot(x, [mf_tri(i, 0.7, 1, 1) for i in x], label="VL")
    plt.legend()
    plt.grid()
    plt.show()


def plot_3d_surface():
    from mpl_toolkits.mplot3d import Axes3D

    X = np.linspace(0, 1, 30)
    Y = np.linspace(0, 1, 30)
    Z = np.zeros((30, 30))

    for i in range(30):
        for j in range(30):
            Z[i, j], _, _ = fuzzy_inference(X[i], Y[j])

    X, Y = np.meshgrid(X, Y)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_title("Fuzzy Inference Surface")
    ax.set_xlabel("Sludge")
    ax.set_ylabel("Grease")
    ax.set_zlabel("Washing Time")
    plt.show()

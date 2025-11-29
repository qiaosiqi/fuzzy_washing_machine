# mfs.py
import numpy as np

EPS = 1e-9

def trap(x, a, b, c, d):
    # vector or scalar safe trapezoid
    x = np.array(x)
    y = np.zeros_like(x, dtype=float)
    # rising
    idx = (x > a) & (x < b)
    if b - a != 0:
        y[idx] = (x[idx] - a) / (b - a)
    # plateau
    idx2 = (x >= b) & (x <= c)
    y[idx2] = 1.0
    # falling
    idx3 = (x > c) & (x < d)
    if d - c != 0:
        y[idx3] = (d - x[idx3]) / (d - c)
    # edges already zero
    return np.clip(y, 0, 1)

def tri(x, a, b, c):
    x = np.array(x)
    y = np.zeros_like(x, dtype=float)
    # rising
    idx = (x >= a) & (x <= b)
    if b - a != 0:
        y[idx] = (x[idx] - a) / (b - a)
    # falling
    idx2 = (x >= b) & (x <= c)
    if c - b != 0:
        y[idx2] = (c - x[idx2]) / (c - b)
    return np.clip(y, 0, 1)

def gauss(x, mean, sigma):
    x = np.array(x, dtype=float)
    return np.exp(-0.5 * ((x - mean) / (sigma + EPS))**2)

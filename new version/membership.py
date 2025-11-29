# membership.py
import numpy as np

def mf_trap(x, a, b, c, d):
    if x <= a or x >= d:
        return 0
    elif b <= x <= c:
        return 1
    elif a < x < b:
        return (x - a) / (b - a + 1e-6)
    else:
        return (d - x) / (d - c + 1e-6)


def mf_tri(x, a, b, c):
    return max(min((x - a) / (b - a + 1e-6), (c - x) / (c - b + 1e-6)), 0)

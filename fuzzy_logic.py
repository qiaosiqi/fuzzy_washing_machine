# fuzzy_logic.py
import numpy as np
from rules import rules

# -------- 梯形隶属函数（不会除零） ----------
def mf_trap(x, a, b, c, d):
    if x <= a or x >= d:
        return 0
    elif b <= x <= c:
        return 1
    elif a < x < b:
        return (x - a) / (b - a + 1e-6)
    else:
        return (d - x) / (d - c + 1e-6)


# -------- 输入变量的隶属度 ----------
def sludge_mf(x):
    return {
        "SD": mf_trap(x, 0, 0, 0.2, 0.4),
        "MD": mf_trap(x, 0.2, 0.4, 0.6, 0.8),
        "LD": mf_trap(x, 0.6, 0.8, 1, 1)
    }


def grease_mf(x):
    return {
        "NG": mf_trap(x, 0, 0, 0.2, 0.4),
        "MG": mf_trap(x, 0.2, 0.4, 0.6, 0.8),
        "LG": mf_trap(x, 0.6, 0.8, 1, 1)
    }


# -------- 输出（时间）的清晰值 ----------
def time_mf():
    return {
        "VS": 0.1,
        "S": 0.3,
        "M": 0.5,
        "L": 0.7,
        "VL": 0.9
    }


# -------- 模糊推理 ----------
def fuzzy_inference(sludge_val, grease_val):
    sludge_degree = sludge_mf(sludge_val)
    grease_degree = grease_mf(grease_val)
    time_values = time_mf()

    result = []
    for (x_label, y_label, z_label) in rules:
        firing = min(sludge_degree[x_label], grease_degree[y_label])
        crisp_output = firing * time_values[z_label]
        result.append(crisp_output)

    return max(result), sludge_degree, grease_degree

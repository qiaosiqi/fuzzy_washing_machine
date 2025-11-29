# logic.py
from membership import mf_trap
from rules import rules

def sludge_mf(x):
    return {
        "SD": mf_trap(x, 0, 0, 0.2, 0.4),
        "MD": mf_trap(x, 0.2, 0.4, 0.6, 0.8),
        "LD": mf_trap(x, 0.6, 0.8, 1, 1)
    }

def grease_mf(x):
    # 返回与规则匹配的键名：NG, MG, LG
    return {
        "NG": mf_trap(x, 0, 0, 0.2, 0.4),
        "MG": mf_trap(x, 0.2, 0.4, 0.6, 0.8),
        "LG": mf_trap(x, 0.6, 0.8, 1, 1)
    }

def time_mf():
    return {
        "VS": 0.1,
        "S": 0.3,
        "M": 0.5,
        "L": 0.7,
        "VL": 0.9
    }

def fuzzy_inference(sludge_val, grease_val):
    s_deg = sludge_mf(sludge_val)
    g_deg = grease_mf(grease_val)
    time_val = time_mf()

    result_values = []
    for x_label, y_label, z_label in rules:
        firing = min(s_deg[x_label], g_deg[y_label])
        crisp = firing * time_val[z_label]
        result_values.append(crisp)

    return max(result_values), s_deg, g_deg

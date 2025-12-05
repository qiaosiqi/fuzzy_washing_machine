# fuzzy_core.py
# 核心模糊推理模块：隶属函数，规则库，推理 (Mamdani max-min, max-product, Sugeno)
import numpy as np

# 语言集合（时间标签对应数值中心）
TIME_LABELS = ['VS', 'S', 'M', 'L', 'VL']
TIME_CENTERS = {'VS':0.0, 'S':0.25, 'M':0.5, 'L':0.75, 'VL':1.0}

def tri_mf(x, a, b, c):
    """三角隶属函数"""
    x = np.asarray(x)
    y = np.zeros_like(x, dtype=float)
    left = (a < x) & (x <= b)
    right = (b < x) & (x < c)
    if b != a:
        y[left] = (x[left] - a) / (b - a)
    if c != b:
        y[right] = (c - x[right]) / (c - b)
    y[x == b] = 1.0
    return y

# 定义污泥与油脂的隶属函数参数（三角）
# SD peak at 0, MD peak at 0.5, LD peak at 1.0
SLUDGE_MFS = {
    'SD': lambda x: tri_mf(x, -0.1, 0.0, 0.5),   # support [-0.1,0.5], peak 0
    'MD': lambda x: tri_mf(x, 0.0, 0.5, 1.0),    # peak 0.5
    'LD': lambda x: tri_mf(x, 0.5, 1.0, 1.1)     # support [0.5,1.1], peak 1.0
}
GREASE_MFS = {
    'NG': lambda x: tri_mf(x, -0.1, 0.0, 0.5),
    'MG': lambda x: tri_mf(x, 0.0, 0.5, 1.0),
    'LG': lambda x: tri_mf(x, 0.5, 1.0, 1.1)
}
# 时间（输出）隶属函数： centers at 0,0.25,0.5,0.75,1
TIME_MFS = {
    'VS': lambda x: tri_mf(x, -0.1, 0.0, 0.25),
    'S' : lambda x: tri_mf(x, 0.0, 0.25, 0.5),
    'M' : lambda x: tri_mf(x, 0.25, 0.5, 0.75),
    'L' : lambda x: tri_mf(x, 0.5, 0.75, 1.0),
    'VL': lambda x: tri_mf(x, 0.75, 1.0, 1.1)
}

# 规则库： list of (sludge_label, grease_label, time_label)
RULES = [
    ('SD','NG','VS'),
    ('SD','MG','M'),
    ('SD','LG','L'),
    ('MD','NG','S'),
    ('MD','MG','M'),
    ('MD','LG','L'),
    ('LD','NG','M'),
    ('LD','MG','L'),
    ('LD','LG','VL')
]

def fuzzify_inputs(sludge_val, grease_val):
    """返回每个语言标签的隶属度字典"""
    sd = {k: float(v(sludge_val)) for k,v in SLUDGE_MFS.items()}
    gg = {k: float(v(grease_val)) for k,v in GREASE_MFS.items()}
    return sd, gg

def rule_firing_strengths(sludge_val, grease_val, method='maxmin'):
    """
    计算每条规则的触发强度
    method: 'maxmin' (Mamdani with min for antecedent), 'maxprod' (product)
    返回 list of firing strengths aligned with RULES
    """
    sd, gg = fuzzify_inputs(sludge_val, grease_val)
    strengths = []
    for (s_label, g_label, t_label) in RULES:
        a = sd[s_label]
        b = gg[g_label]
        if method == 'maxmin':
            f = min(a, b)
        elif method == 'maxprod':
            f = a * b
        else:
            raise ValueError("method must be 'maxmin' or 'maxprod'")
        strengths.append(float(f))
    return strengths

def mamdani_aggregate(sludge_val, grease_val, antecedent='maxmin'):
    """
    执行 Mamdani 推理（聚合输出隶属度函数）。
    返回 aggregated_mu(x) over a fine grid and the grid.
    """
    strengths = rule_firing_strengths(sludge_val, grease_val, method=antecedent)
    # x grid for time
    x = np.linspace(0.0, 1.0, 201)
    agg = np.zeros_like(x)
    for (f, rule) in zip(strengths, RULES):
        out_label = rule[2]
        mu = TIME_MFS[out_label](x)
        # implication using min (clipping to firing strength)
        clipped = np.minimum(mu, f)
        agg = np.maximum(agg, clipped)  # aggregation by max
    return x, agg

def centroid_defuzz(x, mu):
    denom = np.sum(mu)
    if denom == 0:
        return 0.0
    return float(np.sum(x * mu) / denom)

def max_membership_defuzz(x, mu):
    idx = np.argmax(mu)
    return float(x[idx])

def sugeno_inference(sludge_val, grease_val):
    """
    0th-order Sugeno: each rule consequent is a constant (centers).
    result = sum(w_i * z_i) / sum(w_i), where w_i is firing strength, z_i is constant center
    """
    strengths = rule_firing_strengths(sludge_val, grease_val, method='maxprod')  # often use product
    z_values = [TIME_CENTERS[rule[2]] for rule in RULES]
    strengths = np.array(strengths, dtype=float)
    z_values = np.array(z_values, dtype=float)
    denom = np.sum(strengths)
    if denom == 0:
        return 0.0, strengths
    return float(np.sum(strengths * z_values) / denom), strengths

def inference(sludge_val, grease_val,
              engine='mamdani', antecedent='maxmin', defuzz='centroid'):
    """
    公共接口：
    engine: 'mamdani' or 'sugeno'
    antecedent: 'maxmin' or 'maxprod' (only for mamdani antecedent combining)
    defuzz: 'centroid' or 'max' (only for mamdani); for sugeno, defuzz ignored
    返回 (result_value, linguistic_label, debug_info)
    debug_info 包含：firing_strengths, aggregated x, mu (for plotting)
    """
    if engine == 'sugeno':
        val, strengths = sugeno_inference(sludge_val, grease_val)
        # find nearest linguistic label by center distance
        label = min(TIME_LABELS, key=lambda L: abs(val - TIME_CENTERS[L]))
        debug = {'strengths': strengths, 'engine':'sugeno'}
        return val, label, debug

    # mamdani
    x, agg = mamdani_aggregate(sludge_val, grease_val, antecedent=antecedent)
    if defuzz == 'centroid':
        val = centroid_defuzz(x, agg)
    elif defuzz == 'max':
        val = max_membership_defuzz(x, agg)
    else:
        raise ValueError("defuzz must be 'centroid' or 'max'")
    # find nearest label by center distance
    label = min(TIME_LABELS, key=lambda L: abs(val - TIME_CENTERS[L]))
    debug = {'x': x, 'agg': agg, 'engine':'mamdani', 'antecedent':antecedent, 'defuzz':defuzz,
             'strengths': rule_firing_strengths(sludge_val, grease_val, method=antecedent)}
    return float(val), label, debug

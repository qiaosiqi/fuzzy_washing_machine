# logic.py
import numpy as np
from mfs import trap, tri, gauss
from rules import RULES, SUGENO_VALUES

# Universes normalized [0,1]
U = np.linspace(0,1,201)
U_time = np.linspace(0,60,301)  # actual minutes for plotting/defuzz

# Provide MF sets for different kinds: 'triangular', 'trapezoid', 'gaussian'
def make_mfs(kind="trapezoid"):
    if kind == "trapezoid":
        sludge = {
            "SD": trap(U, 0.0, 0.0, 0.2, 0.4),
            "MD": trap(U, 0.2, 0.4, 0.6, 0.8),
            "LD": trap(U, 0.6, 0.8, 1.0, 1.0)
        }
        grease = {
            "NG": trap(U, 0.0, 0.0, 0.2, 0.4),
            "MG": trap(U, 0.2, 0.4, 0.6, 0.8),
            "LG": trap(U, 0.6, 0.8, 1.0, 1.0)
        }
        time = {
            "VS": tri(U, 0.0, 0.0, 0.2),
            "S":  tri(U, 0.1, 0.3, 0.5),
            "M":  tri(U, 0.3, 0.5, 0.7),
            "L":  tri(U, 0.5, 0.7, 0.9),
            "VL": tri(U, 0.7, 1.0, 1.0)
        }
    elif kind == "triangular":
        sludge = {
            "SD": tri(U, 0.0, 0.0, 0.5),
            "MD": tri(U, 0.25, 0.5, 0.75),
            "LD": tri(U, 0.5, 1.0, 1.0)
        }
        grease = {
            "NG": tri(U, 0.0, 0.0, 0.5),
            "MG": tri(U, 0.25, 0.5, 0.75),
            "LG": tri(U, 0.5, 1.0, 1.0)
        }
        time = {
            "VS": tri(U, 0, 0, 0.25),
            "S": tri(U, 0.15, 0.3, 0.45),
            "M": tri(U, 0.35, 0.5, 0.65),
            "L": tri(U, 0.55, 0.7, 0.85),
            "VL": tri(U, 0.7, 1, 1)
        }
    elif kind == "gaussian":
        sludge = {"SD": gauss(U,0,0.18), "MD": gauss(U,0.5,0.15), "LD": gauss(U,1,0.18)}
        grease = {"NG": gauss(U,0,0.18), "MG": gauss(U,0.5,0.15), "LG": gauss(U,1,0.18)}
        time = {"VS": gauss(U,0,0.07), "S": gauss(U,0.2,0.08), "M": gauss(U,0.45,0.09), "L": gauss(U,0.7,0.09), "VL": gauss(U,0.95,0.06)}
    else:
        raise ValueError("Unknown MF kind")
    return sludge, grease, time

# fuzzify a crisp value (0..1)
def fuzzify_single(value, universe, mfs):
    return {name: float(np.interp(value, universe, mf)) for name, mf in mfs.items()}

# Mamdani inference: aggregation via clipping (min), combine via max, defuzzify methods supported
def mamdani_infer(sludge_val, grease_val, mf_kind="trapezoid", defuzz="centroid"):
    sludge_mfs, grease_mfs, time_mfs = make_mfs(mf_kind)
    mu_s = fuzzify_single(sludge_val, U, sludge_mfs)
    mu_g = fuzzify_single(grease_val, U, grease_mfs)
    # rule firing
    firings = []
    for (sx, gy, tz) in RULES:
        alpha = min(mu_s[sx], mu_g[gy])
        firings.append({"if":(sx,gy),"then":tz,"alpha":alpha})
    # aggregate by clipping each output mf by rule alpha and taking max across rules
    aggregated = np.zeros_like(U)
    for f in firings:
        out_mf = time_mfs[f["then"]]
        clipped = np.minimum(out_mf, f["alpha"])
        aggregated = np.maximum(aggregated, clipped)
    # defuzzify
    # mapping U (0..1) -> minutes 0..60
    minutes = U_time_map(U)
    if defuzz == "centroid":
        if aggregated.sum() == 0:
            z = 0.0
        else:
            z = float(np.sum(aggregated * minutes) / np.sum(aggregated))
    elif defuzz == "bisector":
        # bisector: find point that splits area into halves
        area = np.sum(aggregated)
        if area == 0:
            z = 0.0
        else:
            cum = np.cumsum(aggregated)
            idx = np.searchsorted(cum, area/2.0)
            z = float(minutes[idx])
    elif defuzz == "mom":  # mean of maxima
        maxv = aggregated.max()
        if maxv <= 0:
            z = 0.0
        else:
            idxs = np.where(aggregated >= maxv - 1e-9)[0]
            z = float(np.mean(minutes[idxs]))
    else:
        raise ValueError("Unknown defuzz method")
    return {"mu_s":mu_s, "mu_g":mu_g, "firings":firings, "aggregated":aggregated, "z":z}

# Sugeno inference (zero order): weighted average of rule constants
def sugeno_infer(sludge_val, grease_val, mf_kind="trapezoid"):
    sludge_mfs, grease_mfs, _ = make_mfs(mf_kind)
    mu_s = fuzzify_single(sludge_val, U, sludge_mfs)
    mu_g = fuzzify_single(grease_val, U, grease_mfs)
    numerator = 0.0; denom = 0.0
    firings = []
    for (sx, gy, tz) in RULES:
        alpha = min(mu_s[sx], mu_g[gy])
        v = SUGENO_VALUES[tz]
        numerator += alpha * v
        denom += alpha
        firings.append({"if":(sx,gy),"then":tz,"alpha":alpha,"v":v})
    z = numerator/denom if denom != 0 else 0.0
    return {"mu_s":mu_s,"mu_g":mu_g,"firings":firings,"z":z}

# helper to map normalized U to minutes [0,60]
def U_time_map(U_normalized):
    return U_normalized * 60.0

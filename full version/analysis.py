# analysis.py
import pandas as pd
from logic import mamdani_infer, sugeno_infer
import os
OUT="outputs"
os.makedirs(OUT, exist_ok=True)

def run_comparison_grid(s_vals=None, g_vals=None, mf_kinds=("trapezoid","triangular","gaussian"), methods=("Mamdani_centroid","Sugeno")):
    if s_vals is None:
        s_vals = [0.0, 0.15, 0.3, 0.5, 0.7, 0.9]
    if g_vals is None:
        g_vals = [0.0, 0.15, 0.3, 0.5, 0.7, 0.9]
    rows=[]
    for mf in mf_kinds:
        for s in s_vals:
            for g in g_vals:
                r={}
                r.update({"mf_kind":mf,"sludge":s,"grease":g})
                # Mamdani centroid
                outm = mamdani_infer(s,g,mf,"centroid")
                r["Mamdani_centroid"]=outm["z"]
                # Mamdani bisector
                r["Mamdani_bisector"]=mamdani_infer(s,g,mf,"bisector")["z"]
                # Sugeno
                r["Sugeno"]=sugeno_infer(s,g,mf)["z"]
                rows.append(r)
    df = pd.DataFrame(rows)
    csv = os.path.join(OUT,"comparison_grid.csv")
    df.to_csv(csv,index=False)
    # basic stats
    stats = df.describe()
    stats_path = os.path.join(OUT,"comparison_stats.csv")
    stats.to_csv(stats_path)
    return csv, stats_path, df

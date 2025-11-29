# plots.py
import matplotlib.pyplot as plt
import numpy as np
from logic import make_mfs, U_time_map, U
from mpl_toolkits.mplot3d import Axes3D
import os
OUT="outputs"
os.makedirs(OUT, exist_ok=True)

def plot_mfs(kind="trapezoid"):
    sludge_mfs, grease_mfs, time_mfs = make_mfs(kind)
    x = U
    plt.figure(figsize=(8,3))
    for name,mf in sludge_mfs.items(): plt.plot(x, mf, label=name)
    plt.title(f"Sludge MFs ({kind})"); plt.legend(); plt.grid(True); plt.tight_layout()
    p1 = os.path.join(OUT, f"sludge_mfs_{kind}.png"); plt.savefig(p1); plt.close()

    plt.figure(figsize=(8,3))
    for name,mf in grease_mfs.items(): plt.plot(x, mf, label=name)
    plt.title(f"Grease MFs ({kind})"); plt.legend(); plt.grid(True); plt.tight_layout()
    p2 = os.path.join(OUT, f"grease_mfs_{kind}.png"); plt.savefig(p2); plt.close()

    plt.figure(figsize=(8,3))
    for name,mf in time_mfs.items(): plt.plot(x, mf, label=name)
    plt.title(f"Time MFs ({kind})"); plt.legend(); plt.grid(True); plt.tight_layout()
    p3 = os.path.join(OUT, f"time_mfs_{kind}.png"); plt.savefig(p3); plt.close()
    return p1,p2,p3

def plot_aggregated(aggregated, file_name="aggregated.png"):
    minutes = U_time_map(U)
    plt.figure(figsize=(8,3))
    plt.plot(minutes, aggregated, label="Aggregated")
    plt.title("Aggregated output (Mamdani)")
    plt.xlabel("Time (min)"); plt.ylabel("Degree"); plt.grid(True); plt.tight_layout()
    p = os.path.join(OUT, file_name); plt.savefig(p); plt.close(); return p

def plot_surface(mf_kind="trapezoid", res=41, out_name="surface.png"):
    s = np.linspace(0,1,res); g = np.linspace(0,1,res)
    Z = np.zeros((res,res))
    from logic import mamdani_infer
    for i,sv in enumerate(s):
        for j,gv in enumerate(g):
            Z[i,j] = mamdani_infer(sv,gv,mf_kind)["z"]
    Sg,Gg = np.meshgrid(s,g)
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(Sg, Gg, Z, cmap='viridis', edgecolor='none')
    ax.set_xlabel("Sludge"); ax.set_ylabel("Grease"); ax.set_zlabel("Time (min)")
    p = os.path.join(OUT, out_name); plt.tight_layout(); fig.savefig(p); plt.close(); return p

def plot_comparison_heatmap(csv_df, col_name, out_name):
    # csv_df: pandas DataFrame pivotable
    import pandas as pd
    pivot = csv_df.pivot(index="sludge", columns="grease", values=col_name)
    plt.figure(figsize=(6,5))
    plt.imshow(pivot.values, origin='lower', aspect='auto')
    plt.colorbar(label='Time(min)')
    plt.title(col_name)
    p = os.path.join(OUT, out_name); plt.tight_layout(); plt.savefig(p); plt.close(); return p

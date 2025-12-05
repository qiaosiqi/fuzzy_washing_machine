# viz.py
# 可视化：membership plots, 3D surface of inference results, history plots
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from fuzzy_core import SLUDGE_MFS, GREASE_MFS, TIME_MFS, TIME_LABELS, TIME_CENTERS
from fuzzy_core import inference

def plot_membership_functions():
    x = np.linspace(0,1,201)
    fig, axs = plt.subplots(1,3, figsize=(15,4))
    # sludge
    for k,f in SLUDGE_MFS.items():
        axs[0].plot(x, f(x), label=k)
    axs[0].set_title('Sludge membership')
    axs[0].legend()
    # grease
    for k,f in GREASE_MFS.items():
        axs[1].plot(x, f(x), label=k)
    axs[1].set_title('Grease membership')
    axs[1].legend()
    # time
    for k,f in TIME_MFS.items():
        axs[2].plot(x, f(x), label=k)
    axs[2].set_title('Time membership')
    axs[2].legend()
    plt.tight_layout()
    return fig

def plot_3d_surface(engine='mamdani', antecedent='maxmin', defuzz='centroid', res=31):
    s_vals = np.linspace(0,1,res)
    g_vals = np.linspace(0,1,res)
    S, G = np.meshgrid(s_vals, g_vals)
    Z = np.zeros_like(S)
    for i in range(S.shape[0]):
        for j in range(S.shape[1]):
            s = S[i,j]
            g = G[i,j]
            if engine == 'sugeno':
                val, _, _ = inference(s,g, engine='sugeno')
            else:
                val, _, _ = inference(s,g, engine='mamdani', antecedent=antecedent, defuzz=defuzz)
            Z[i,j] = val
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(S, G, Z, cmap='viridis', edgecolor='none')
    ax.set_xlabel('Sludge')
    ax.set_ylabel('Grease')
    ax.set_zlabel('Wash time (0-1)')
    ax.set_title(f'Inference surface: {engine}/{antecedent}/{defuzz}')
    return fig

def plot_history_stats(df):
    # expects pandas df with columns ['created_at','result_time']
    import pandas as pd
    if df.empty:
        fig, ax = plt.subplots(figsize=(6,3))
        ax.text(0.5,0.5,"No data", ha='center')
        return fig
    df2 = df.copy()
    df2['created_at'] = pd.to_datetime(df2['created_at'])
    df2 = df2.sort_values('created_at')
    fig, ax = plt.subplots(figsize=(8,3))
    ax.plot(df2['created_at'], df2['result_time'], marker='o')
    ax.set_title('Historical result_time trend')
    ax.set_ylabel('Time (0-1)')
    fig.autofmt_xdate()
    return fig

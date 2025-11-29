# app_gui.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import uuid
from logic import mamdani_infer, sugeno_infer
from db import init_db, save_run, list_runs, delete_run
from plots import plot_mfs, plot_surface, plot_aggregated
from analysis import run_comparison_grid
import os, pandas as pd

OUT="outputs"
os.makedirs(OUT, exist_ok=True)
init_db()

def make_main_window():
    root = ttk.Window(themename="darkly")
    root.title("智能洗衣机 — 模糊控制实验")
    root.geometry("900x600")

    # left frame - controls
    left = ttk.Frame(root, padding=12)
    left.pack(side="left", fill="y")

    ttk.Label(left, text="污泥 (0..1)").pack(pady=(4,0))
    s_scale = ttk.Scale(left, from_=0, to=1, bootstyle="secondary", length=260)
    s_scale.set(0.5); s_scale.pack(pady=6)

    ttk.Label(left, text="油脂 (0..1)").pack(pady=(4,0))
    g_scale = ttk.Scale(left, from_=0, to=1, bootstyle="secondary", length=260)
    g_scale.set(0.5); g_scale.pack(pady=6)

    ttk.Label(left, text="MF 类型").pack(pady=(8,0))
    mf_choice = ttk.Combobox(left, values=["trapezoid","triangular","gaussian"]); mf_choice.set("trapezoid"); mf_choice.pack()

    ttk.Label(left, text="推理方法").pack(pady=(8,0))
    method = ttk.Combobox(left, values=["Mamdani_centroid","Mamdani_bisector","Mamdani_mom","Sugeno"]); method.set("Mamdani_centroid"); method.pack()

    result_var = ttk.StringVar(value="结果：等待运行")
    result_label = ttk.Label(left, textvariable=result_var, font=("Helvetica",14))
    result_label.pack(pady=12)

    def run_once():
        s = float(s_scale.get()); g = float(g_scale.get())
        mfk = mf_choice.get()
        m = method.get()
        if m.startswith("Mamdani"):
            defuzz = "centroid" if "centroid" in m else ("bisector" if "bisector" in m else "mom")
            out = mamdani_infer(s,g,mfk,defuzz)
            aggregated = out["aggregated"]
            plot_aggregated(aggregated, file_name=f"aggregated_run_{int(uuid.uuid4().int % 1000000)}.png")
            z = out["z"]
            firings = out["firings"]
            save_run(s,g,"Mamdani",mfk,defuzz,z,firings)
        else:
            out = sugeno_infer(s,g,mfk)
            z = out["z"]; firings = out["firings"]
            save_run(s,g,"Sugeno",mfk,"-",z,firings)
        result_var.set(f"结果：{z:.2f} min")
        refresh_history()

    ttk.Button(left, text="开始推理并保存", bootstyle=SUCCESS, command=run_once).pack(pady=6)
    ttk.Button(left, text="显示隶属函数图", bootstyle=INFO, command=lambda: plot_mfs(mf_choice.get())).pack(pady=4)
    ttk.Button(left, text="显示推理曲面(慢)", bootstyle=INFO, command=lambda: plot_surface(mf_choice.get(), out_name="surface.png")).pack(pady=4)
    ttk.Button(left, text="运行对比实验(慢)", bootstyle=SECONDARY, command=lambda: run_and_show_comparison()).pack(pady=6)

    # right frame - history and details
    right = ttk.Frame(root, padding=12)
    right.pack(side="left", fill="both", expand=True)
    ttk.Label(right, text="历史记录（最近）").pack()
    cols = ("id","ts","sludge","grease","method","mf_kind","defuzz","result")
    tree = ttk.Treeview(right, columns=cols, show="headings", height=18)
    for c in cols: tree.heading(c, text=c)
    tree.pack(fill="both", expand=True, pady=6)

    btn_frame = ttk.Frame(right)
    btn_frame.pack()
    def refresh_history():
        for it in tree.get_children(): tree.delete(it)
        rows = list_runs(200)
        for r in rows: tree.insert("", "end", values=r)
    def delete_selected():
        sel = tree.selection()
        for s in sel:
            rid = tree.item(s)["values"][0]
            delete_run(rid)
        refresh_history()
    ttk.Button(btn_frame, text="刷新", command=refresh_history).pack(side="left", padx=6)
    ttk.Button(btn_frame, text="删除选中", command=delete_selected, bootstyle="danger").pack(side="left", padx=6)
    refresh_history()

    def run_and_show_comparison():
        csv, stats, df = run_comparison_grid()
        # save CSV and show a simple message and open with pandas for preview
        dfp = df.pivot_table(index="sludge", columns="grease", values="Mamdani_centroid")
        # show a small preview window
        preview = ttk.Toplevel(root)
        preview.title("Comparison preview (Mamdani_centroid)")
        txt = ttk.Text(preview, width=80, height=30)
        txt.insert("1.0", dfp.round(2).to_string())
        txt.pack()
        # also save plots via plots.plot_comparison_heatmap if desired

    return root

if __name__ == "__main__":
    win = make_main_window()
    win.mainloop()

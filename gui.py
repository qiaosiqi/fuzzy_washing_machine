# gui.py
import tkinter as tk
from tkinter import ttk, messagebox

from fuzzy_logic import fuzzy_inference
from database import insert_record, fetch_records, delete_record
from plot_utils import plot_membership_functions, plot_3d_rules


class WashingGUI:
    def __init__(self, root):
        root.title("洗衣机模糊控制系统")
        root.geometry("600x500")

        ttk.Label(root, text="污泥程度（0~1）").pack()
        self.sludge_var = tk.DoubleVar()
        ttk.Entry(root, textvariable=self.sludge_var).pack()

        ttk.Label(root, text="油脂程度（0~1）").pack()
        self.grease_var = tk.DoubleVar()
        ttk.Entry(root, textvariable=self.grease_var).pack()

        ttk.Button(root, text="开始推理", command=self.run_inference).pack(pady=10)
        ttk.Button(root, text="查看隶属函数图", command=plot_membership_functions).pack()
        ttk.Button(root, text="查看推理立体图", command=plot_3d_rules).pack(pady=5)
        ttk.Button(root, text="显示数据库记录", command=self.show_db).pack()

        self.result_label = ttk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)

    def run_inference(self):
        s = self.sludge_var.get()
        g = self.grease_var.get()

        value, _, _ = fuzzy_inference(s, g)
        self.result_label.config(text=f"推理洗涤时间结果：{value:.3f}")

        insert_record(s, g, value)

    def show_db(self):
        records = fetch_records()
        msg = "\n".join([str(r) for r in records])
        messagebox.showinfo("数据库记录", msg if msg else "数据库空无记录")

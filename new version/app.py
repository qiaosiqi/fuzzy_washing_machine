# app.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from logic import fuzzy_inference
from plotting import plot_input_membership, plot_output_membership, plot_3d_surface


def run_app():
    root = ttk.Window(themename="darkly")
    root.title("智能洗衣机模糊控制系统")
    root.geometry("550x450")

    ttk.Label(root, text="污泥 (0〜1)", font=("微软雅黑", 12)).pack(pady=10)
    sludge_slider = ttk.Scale(root, from_=0, to=1, length=300)
    sludge_slider.pack()

    ttk.Label(root, text="油脂 (0〜1)", font=("微软雅黑", 12)).pack(pady=10)
    grease_slider = ttk.Scale(root, from_=0, to=1, length=300)
    grease_slider.pack()

    result_label = ttk.Label(root, text="等待推理...", font=("微软雅黑", 14))
    result_label.pack(pady=15)

    def start_inference():
        s = sludge_slider.get()
        g = grease_slider.get()
        res, _, _ = fuzzy_inference(s, g)
        result_label.config(text=f"预测洗涤时间：{res:.3f}")

    ttk.Button(root, text="开始推理", bootstyle=SUCCESS, command=start_inference).pack(pady=10)

    ttk.Button(root, text="输入隶属函数图", bootstyle=INFO, command=plot_input_membership).pack(pady=5)
    ttk.Button(root, text="输出隶属函数图", bootstyle=INFO, command=plot_output_membership).pack(pady=5)
    ttk.Button(root, text="推理3D图", bootstyle=WARNING, command=plot_3d_surface).pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    run_app()

# main.py
import sys
from db import init_db
from app_gui import make_main_window
from analysis import run_comparison_grid
from plots import plot_mfs, plot_surface

def print_help():
    print("Usage: python main.py [gui|compare|plots]")
    print("  gui     : launch GUI")
    print("  compare : run comparison experiments (csv & stats to outputs/)")
    print("  plots   : generate membership & surface plots")

if __name__ == "__main__":
    init_db()
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "gui":
            win = make_main_window()
            win.mainloop()
        elif cmd == "compare":
            csv, stats, df = run_comparison_grid()
            print("Comparison saved:", csv, stats)
        elif cmd == "plots":
            plot_mfs("trapezoid")
            plot_surface("trapezoid", out_name="surface.png")
            print("Plots generated in outputs/")
        else:
            print_help()
    else:
        print_help()

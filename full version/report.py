# report.py
from fpdf import FPDF
import os
def make_pdf_report(outdir="outputs", pdfname="fuzzy_report.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Fuzzy Washing Machine Experiment Report", 0, 1, 'C')
    pdf.ln(4)
    pdf.set_font("Arial","",11)
    pdf.multi_cell(0,6,"This report contains membership function plots, inference surface, and comparison results.")
    # attach images if exist
    imgs = ["sludge_mfs_trapezoid.png","grease_mfs_trapezoid.png","time_mfs_trapezoid.png","surface.png","comparison_grid.csv"]
    for im in imgs:
        p = os.path.join(outdir, im)
        if os.path.exists(p) and p.endswith(".png"):
            pdf.add_page()
            pdf.image(p, x=10, y=20, w=190)
    outpdf = os.path.join(outdir, pdfname)
    pdf.output(outpdf)
    return outpdf

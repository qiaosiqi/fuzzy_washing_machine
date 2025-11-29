# rules.py

# 模糊规则矩阵（字典形式，便于维护）
# x: sludge, y: grease, z: time
# SD/MD/LD ; NG/MG/LG ; VS/S/M/L/VL
rules = [
    ("SD", "NG", "VS"),
    ("SD", "MG", "M"),
    ("SD", "LG", "L"),
    ("MD", "NG", "S"),
    ("MD", "MG", "M"),
    ("MD", "LG", "L"),
    ("LD", "NG", "M"),
    ("LD", "MG", "L"),
    ("LD", "LG", "VL")
]

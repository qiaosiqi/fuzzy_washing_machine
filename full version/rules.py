# rules.py
# fuzzy rules: sludge x grease -> time
RULES = [
    ("SD","NG","VS"),
    ("SD","MG","M"),
    ("SD","LG","L"),
    ("MD","NG","S"),
    ("MD","MG","M"),
    ("MD","LG","L"),
    ("LD","NG","M"),
    ("LD","MG","L"),
    ("LD","LG","VL"),
]
# Labels for time (for Sugeno crisp values)
SUGENO_VALUES = {"VS":3.0,"S":10.0,"M":25.0,"L":40.0,"VL":55.0}

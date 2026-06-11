# -*- coding: utf-8 -*-
import os

index_path = r"c:\Users\lap4all\Desktop\New folder\templates\index.html"

queries = [
    "tab-ntb-summary",
    "tab-opr",
    "switchNtbRegion",
    "renderNtbKpiCards",
    "loadNtbSummaryData",
    "renderOprDashboard",
    "setAmOprSort"
]

with open(index_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Total lines in index.html:", len(lines))

for q in queries:
    matches = []
    for idx, line in enumerate(lines):
        if q in line:
            matches.append(idx + 1)
    print(f"Query '{q}' matches at lines: {matches[:15]}")

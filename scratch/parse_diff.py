# -*- coding: utf-8 -*-
import os

diff_path = r"c:\Users\lap4all\Desktop\New folder\scratch\git_diff_index.txt"

with open(diff_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Total lines in diff:", len(lines))

added_lines = []
deleted_lines = []

for line in lines:
    if line.startswith("+") and not line.startswith("+++"):
        added_lines.append(line)
    elif line.startswith("-") and not line.startswith("---"):
        deleted_lines.append(line)

print("Added lines count:", len(added_lines))
print("Deleted lines count:", len(deleted_lines))

# Search for interesting keywords in added or deleted lines
keywords = ["switchNtbRegion", "renderNtbKpiCards", "renderOprDashboard", "setAmOprSort", "renderNtbAnalysisTable"]
for kw in keywords:
    adds = [l for l in added_lines if kw in l]
    dels = [l for l in deleted_lines if kw in l]
    print(f"Keyword: '{kw}'")
    print(f"  Added occurrences: {len(adds)}")
    print(f"  Deleted occurrences: {len(dels)}")

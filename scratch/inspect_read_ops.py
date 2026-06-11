# -*- coding: utf-8 -*-
with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(r"scratch\read_ops_sheet_lines2.txt", "w", encoding="utf-8") as out:
    for i in range(435, 490):
        if i < len(lines):
            out.write(f"{i+1}: {lines[i]}")
print("Done")

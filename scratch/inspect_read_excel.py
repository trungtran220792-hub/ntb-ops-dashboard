# -*- coding: utf-8 -*-
with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(r"scratch\app_read_excel.txt", "w", encoding="utf-8") as out:
    for i in range(600, 631):
        if i < len(lines):
            out.write(f"{i+1}: {lines[i]}")
print("Done")

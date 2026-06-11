# -*- coding: utf-8 -*-
with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(r"scratch\ltc_vol_lines.txt", "w", encoding="utf-8") as out:
    for i in range(630, 670):
        if i < len(lines):
            out.write(f"{i+1}: {lines[i]}")
print("Done")

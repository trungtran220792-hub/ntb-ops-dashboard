# -*- coding: utf-8 -*-
with open("templates/index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(r"scratch\switch_tab_def.txt", "w", encoding="utf-8") as out:
    for i in range(3340, 3420):
        if i < len(lines):
            out.write(f"{i+1}: {lines[i]}")
print("Done")

# -*- coding: utf-8 -*-
with open("templates/index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(r"scratch\gate_menu_tabs_inspect.txt", "w", encoding="utf-8") as out:
    for i in range(3460, 3515):
        if i < len(lines):
            out.write(f"{i+1}: {lines[i]}")
print("Done")

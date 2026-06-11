# -*- coding: utf-8 -*-
with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(r"scratch\ltc_vol_error_inspect.txt", "w", encoding="utf-8") as out:
    for i in range(645, 680):
        if i < len(lines):
            out.write(f"{i+1}: {repr(lines[i])}\n")
print("Done")

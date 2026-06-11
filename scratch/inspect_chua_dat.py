# -*- coding: utf-8 -*-
with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(r"scratch\chua_dat_search.txt", "w", encoding="utf-8") as out:
    for idx, line in enumerate(lines):
        if "chưa đạt" in line or "chua dat" in line:
            out.write(f"Line {idx+1}: {line.strip()}\n")
print("Done")

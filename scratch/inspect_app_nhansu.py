# -*- coding: utf-8 -*-
with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(r"scratch\inspect_app_nhansu_output.txt", "w", encoding="utf-8") as out:
    for idx, line in enumerate(lines):
        if "nhan" in line or "nhan-su" in line or "nhan_su" in line:
            out.write(f"Line {idx+1}: {line.strip()}\n")
print("Done")

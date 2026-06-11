# -*- coding: utf-8 -*-
import os

app_path = r"c:\Users\lap4all\Desktop\New folder\app.py"

with open(app_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

start_line = 2406
end_line = start_line + 150

with open(r"c:\Users\lap4all\Desktop\New folder\scratch\api_summary_code.txt", "w", encoding="utf-8") as out:
    for idx in range(start_line - 1, min(len(lines), end_line)):
        out.write(f"{idx+1}: {lines[idx]}")

print("Saved summary API code to scratch/api_summary_code.txt")

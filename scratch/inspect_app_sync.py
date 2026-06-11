# -*- coding: utf-8 -*-
with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(r"scratch\app_sync_lines.txt", "w", encoding="utf-8") as out:
    out.write("=== app.py line 200-350 ===\n")
    for i in range(200, 350):
        if i < len(lines):
            out.write(f"{i+1}: {lines[i]}")
            
    out.write("\n=== app.py line 2200-2470 ===\n")
    for i in range(2200, 2470):
        if i < len(lines):
            out.write(f"{i+1}: {lines[i]}")
print("Done")

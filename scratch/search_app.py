# -*- coding: utf-8 -*-
import os
import re

files = [
    r"c:\Users\lap4all\Desktop\New folder\app.py",
    r"c:\Users\lap4all\Desktop\New folder\scratch\app.py.base"
]

out = open(r"c:\Users\lap4all\Desktop\New folder\scratch\search_app_res.txt", "w", encoding="utf-8")

for p in files:
    if not os.path.exists(p):
        out.write(f"{p} not found\n")
        continue
    out.write(f"\n================ FILE: {os.path.basename(p)} ================\n")
    try:
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(p, 'r', encoding='utf-16') as f:
                content = f.read()
        except Exception as e:
            out.write(f"Error reading {p}: {e}\n")
            continue
    
    # find all lines with @app.route
    lines = content.split('\n')
    route_lines = []
    for i, line in enumerate(lines):
        if "@app.route" in line:
            route_lines.append((i+1, line.strip()))
    
    out.write(f"Total routes found: {len(route_lines)}\n")
    for line_num, r in route_lines:
        def_line = ""
        if line_num < len(lines):
            def_line = lines[line_num].strip()
        out.write(f"Line {line_num}: {r} -> {def_line}\n")
        
out.close()
print("Done searching app routes.")

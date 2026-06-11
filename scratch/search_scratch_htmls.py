# -*- coding: utf-8 -*-
import os

files = [
    r"c:\Users\lap4all\Desktop\New folder\templates\index.html",
    r"c:\Users\lap4all\Desktop\New folder\scratch\index.html.base",
    r"c:\Users\lap4all\Desktop\New folder\scratch\index.html.patched",
    r"c:\Users\lap4all\Desktop\New folder\scratch\render_index.html"
]

out = open(r"c:\Users\lap4all\Desktop\New folder\scratch\search_htmls_res.txt", "w", encoding="utf-8")

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
            
    # Search for lines containing "nhân sự" or "nhan-su" or "nhan_su"
    lines = content.split('\n')
    found_lines = []
    for i, line in enumerate(lines):
        if any(k in line.lower() for k in ["nhân sự", "nhan-su", "nhan_su"]):
            found_lines.append((i+1, line.strip()))
            
    out.write(f"Total occurrences: {len(found_lines)}\n")
    for line_num, l in found_lines[:100]: # print first 100
        out.write(f"Line {line_num}: {l}\n")
        
out.close()
print("Done searching HTMLs.")

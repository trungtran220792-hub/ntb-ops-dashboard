# -*- coding: utf-8 -*-
import os

filepath = r"c:\Users\lap4all\Desktop\New folder\templates\index.html"
outpath = r"c:\Users\lap4all\Desktop\New folder\scratch\current_opr_html.txt"

if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    start = 2410
    end = 2505
    
    with open(outpath, 'w', encoding='utf-8') as out_f:
        for idx in range(start-1, min(end, len(lines))):
            out_f.write(f"{idx+1}: {lines[idx]}")
    print(f"Current OPR HTML extracted to current_opr_html.txt")
else:
    print("templates/index.html not found")

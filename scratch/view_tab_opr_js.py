# -*- coding: utf-8 -*-
import os

filepath = r"c:\Users\lap4all\Desktop\New folder\templates\index.html"
outpath = r"c:\Users\lap4all\Desktop\New folder\scratch\tab_opr_js_current.txt"

if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    start = 4460
    end = 4800
    
    with open(outpath, 'w', encoding='utf-8') as out_f:
        for idx in range(start-1, min(end, len(lines))):
            out_f.write(f"{idx+1}: {lines[idx]}")
    print(f"Current OPR JS extracted to tab_opr_js_current.txt")
else:
    print("templates/index.html not found")

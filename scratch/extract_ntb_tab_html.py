# -*- coding: utf-8 -*-
import os

filepath = r"c:\Users\lap4all\Desktop\New folder\templates\index.html"
outpath = r"c:\Users\lap4all\Desktop\New folder\scratch\ntb_tab_html.txt"

if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # We know tab-ntb-summary is between line 2106 and 2325 (1-indexed)
    with open(outpath, 'w', encoding='utf-8') as out:
        for i in range(2105, 2325):
            if i < len(lines):
                out.write(lines[i])
    print("Saved tab-ntb-summary HTML to ntb_tab_html.txt")
else:
    print("templates/index.html not found")

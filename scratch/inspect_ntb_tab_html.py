# -*- coding: utf-8 -*-
import os

filepath = r"c:\Users\lap4all\Desktop\New folder\scratch\ntb_tab_html.txt"
outpath = r"c:\Users\lap4all\Desktop\New folder\scratch\inspect_ntb_tab_html_res.txt"

if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open(outpath, 'w', encoding='utf-8') as out_f:
        out_f.write(f"File length: {len(content)}\n")
        out_f.write("First 4000 chars:\n")
        out_f.write(content[:4000].replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"'))
        out_f.write("\n\n" + "="*80 + "\n\n")
        out_f.write("Last 4000 chars:\n")
        out_f.write(content[-4000:].replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"'))
    print("Inspection results saved to inspect_ntb_tab_html_res.txt")
else:
    print("ntb_tab_html.txt not found")

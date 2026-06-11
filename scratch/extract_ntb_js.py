# -*- coding: utf-8 -*-
import os

filepath = r"c:\Users\lap4all\Desktop\New folder\scratch\steps_detail_summary.txt"
outpath = r"c:\Users\lap4all\Desktop\New folder\scratch\extracted_ntb_js_from_summary.txt"

if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    idx = 0
    with open(outpath, 'w', encoding='utf-8') as out_f:
        while True:
            idx = content.find("function renderNtbAnalysisTable", idx)
            if idx == -1:
                break
            out_f.write(f"Found function renderNtbAnalysisTable at index {idx}\n")
            out_f.write(content[idx:idx+12000].replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"'))
            out_f.write("\n\n" + "="*80 + "\n\n")
            idx += 30
    print("Extracted JS function to extracted_ntb_js_from_summary.txt")
else:
    print("steps_detail_summary.txt not found")

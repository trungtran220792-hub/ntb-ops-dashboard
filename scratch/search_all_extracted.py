# -*- coding: utf-8 -*-
import os

folder = r"c:\Users\lap4all\Desktop\New folder\scratch\extracted_steps"
files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".txt")]

outpath = r"c:\Users\lap4all\Desktop\New folder\scratch\search_all_extracted_res.txt"

with open(outpath, 'w', encoding='utf-8') as out_f:
    for filepath in files:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        idx = content.find("function renderNtbAnalysisTable")
        if idx != -1:
            out_f.write(f"Found function renderNtbAnalysisTable in {os.path.basename(filepath)} at index {idx}, length of file is {len(content)}\n")
            rep_idx = content.find("--- REPLACEMENT CONTENT ---", idx)
            if rep_idx != -1:
                out_f.write(f"  Found REPLACEMENT CONTENT in this file after function at index {rep_idx}\n")
                snippet = content[rep_idx:rep_idx+2000]
                out_f.write(f"  Snippet:\n{snippet}\n")
            else:
                out_f.write("  No REPLACEMENT CONTENT found after function in this file\n")
            out_f.write("="*40 + "\n")
print("Finished writing to search_all_extracted_res.txt")

# -*- coding: utf-8 -*-
import os

filepath = r"c:\Users\lap4all\Desktop\New folder\scratch\extracted_steps\92726133-7314-4954-9f94-c885d0c26df2_1177.txt"
outpath = r"c:\Users\lap4all\Desktop\New folder\scratch\check_file_end_res.txt"

if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    with open(outpath, 'w', encoding='utf-8') as out_f:
        out_f.write(f"File length: {len(content)}\n")
        rep_idx = content.find("--- REPLACEMENT CONTENT ---")
        if rep_idx != -1:
            out_f.write(f"Replacement length: {len(content) - rep_idx}\n")
            out_f.write("Last 1000 chars:\n")
            out_f.write(content[-1000:])
        else:
            out_f.write("No replacement content header found\n")
else:
    print("File not found")

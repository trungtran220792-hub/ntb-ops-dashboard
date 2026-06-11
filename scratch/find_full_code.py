# -*- coding: utf-8 -*-
import os

filepath = r"c:\Users\lap4all\Desktop\New folder\scratch\extracted_full_index_changes.txt"
out = open(r"c:\Users\lap4all\Desktop\New folder\scratch\full_code_inspect.txt", "w", encoding="utf-8")

if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Let's search for "function renderNtbAnalysisTable"
    idx = 0
    while True:
        idx = content.find("function renderNtbAnalysisTable", idx)
        if idx == -1:
            break
        
        out.write(f"\n=========================================\n")
        out.write(f"FOUND renderNtbAnalysisTable at index {idx}\n")
        out.write(f"=========================================\n")
        
        # print 2000 chars before and 8000 chars after
        start = max(0, idx - 200)
        end = min(len(content), idx + 8000)
        out.write(content[start:end])
        out.write("\n")
        
        idx += 1
else:
    out.write("File not found\n")

out.close()
print("Done")

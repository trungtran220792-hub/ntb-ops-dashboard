# -*- coding: utf-8 -*-
import os

p = r"c:\Users\lap4all\Desktop\New folder\scratch\search_all_results.txt"
res_path = r"c:\Users\lap4all\Desktop\New folder\scratch\view_search_results_res.txt"

if os.path.exists(p):
    with open(p, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    results = []
    for i, line in enumerate(lines):
        if any(kw in line.lower() for kw in ["nhân sự", "nhan_su", "nhan-su"]):
            results.append(f"Line {i+1}: {line.strip()}")
            
    with open(res_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(results))
    print(f"Saved {len(results)} matches to view_search_results_res.txt")
else:
    print(f"{p} not found")

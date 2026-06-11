# -*- coding: utf-8 -*-
import os

p = r"c:\Users\lap4all\Desktop\New folder\scratch\index.html.patched"
res_path = r"c:\Users\lap4all\Desktop\New folder\scratch\search_patched_nhan_res.txt"

if os.path.exists(p):
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    results = []
    for i, line in enumerate(lines):
        if any(k in line.lower() for k in ["nhân", "nhan", "ns", "hr"]):
            results.append(f"Line {i+1}: {line.strip()}")
            
    with open(res_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(results))
    print(f"Saved {len(results)} matches to search_patched_nhan_res.txt")
else:
    print(f"{p} not found")

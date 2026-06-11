# -*- coding: utf-8 -*-
import os
import re

base_path = r"c:\Users\lap4all\Desktop\New folder\scratch\index_base_utf8.html"
res_path = r"c:\Users\lap4all\Desktop\New folder\scratch\trace_mojibake_res.txt"

if os.path.exists(base_path):
    with open(base_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Let's find any occurrences of "nh" (case-insensitive)
    lines = content.split('\n')
    results = []
    for i, line in enumerate(lines):
        if "nh" in line.lower() or "ns" in line.lower() or "hr" in line.lower():
            # Let's only print if it looks like a tab, menu item, or has id/class/onclick
            if any(k in line for k in ["id=", "class=", "onclick=", "tab-", "menu-item", "<li", "<a", "href="]):
                results.append(f"Line {i+1}: {line.strip()}")
                
    with open(res_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(results))
    print(f"Saved {len(results)} results to trace_mojibake_res.txt")
else:
    print(f"{base_path} not found")

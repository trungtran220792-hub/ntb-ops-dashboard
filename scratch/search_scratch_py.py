# -*- coding: utf-8 -*-
import os

scratch_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"
res_path = r"c:\Users\lap4all\Desktop\New folder\scratch\search_scratch_res.txt"

results = []
for root, dirs, files in os.walk(scratch_dir):
    for file in files:
        if file.endswith(('.py', '.txt', '.js', '.json')):
            p = os.path.join(root, file)
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                try:
                    with open(p, 'r', encoding='utf-16') as f:
                        content = f.read()
                except:
                    continue
            
            # Check keywords
            keywords = ["nhân sự", "nhan-su", "nhan_su"]
            found = [kw for kw in keywords if kw in content.lower()]
            if found:
                results.append(f"File: {os.path.relpath(p, scratch_dir)} | Found keywords: {found}")
                
with open(res_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(results))
print(f"Saved search results to search_scratch_res.txt")

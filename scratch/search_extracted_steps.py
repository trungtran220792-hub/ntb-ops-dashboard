# -*- coding: utf-8 -*-
import os

folder = r"c:\Users\lap4all\Desktop\New folder\scratch\extracted_steps"
res_path = r"c:\Users\lap4all\Desktop\New folder\scratch\search_extracted_steps_res.txt"

results = []
if os.path.exists(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            p = os.path.join(root, file)
            with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Check keywords
            keywords = ["gán tất cả", "gán tts", "odr tts", "nhân sự", "nhan_su", "quản lý nhân sự"]
            found = [kw for kw in keywords if kw in content.lower()]
            if found:
                results.append(f"=========================================")
                results.append(f"FILE: {file} | Keywords: {found}")
                results.append(f"=========================================")
                # Print lines containing any of the keywords
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if any(kw in line.lower() for kw in keywords):
                        results.append(f"Line {i+1}: {line.strip()}")
                results.append("\n")
                
    with open(res_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(results))
    print(f"Saved results to search_extracted_steps_res.txt")
else:
    print(f"Folder not found: {folder}")

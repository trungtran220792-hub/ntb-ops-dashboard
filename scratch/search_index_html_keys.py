# -*- coding: utf-8 -*-
import os

filepath = r"c:\Users\lap4all\Desktop\New folder\templates\index.html"
queries = ["sidebar-menu", "NTB", "OPR", "tts", "Chỉ số", "menu-item"]

if os.path.exists(filepath):
    print(f"File size: {os.path.getsize(filepath)} bytes")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for q in queries:
        count = content.lower().count(q.lower())
        print(f"Query '{q}': {count} occurrences")
        
        # print first 3 line numbers
        lines = content.splitlines()
        found = 0
        for i, line in enumerate(lines, 1):
            if q.lower() in line.lower():
                print(f"  Line {i}: {line[:100]}")
                found += 1
                if found >= 3:
                    break
else:
    print("File not found")

# -*- coding: utf-8 -*-
import os

filepath = r"c:\Users\lap4all\Desktop\New folder\templates\index.html"
if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Total lines: {len(lines)}")
    for idx, line in enumerate(lines):
        if '</style>' in line:
            print(f"Line {idx+1}: {line.strip()}")
else:
    print("templates/index.html not found")

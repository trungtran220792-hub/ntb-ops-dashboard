# -*- coding: utf-8 -*-
with open(r'c:\Users\lap4all\Desktop\New folder\templates\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'DOMContentLoaded' in line or 'onload' in line or 'checkUserRole' in line or 'loadAllData' in line:
        if 'function' not in line: # exclude declarations
            print(f"Line {idx+1}: {line.strip()}")

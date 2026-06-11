# -*- coding: utf-8 -*-
import os

filepath = r"c:\Users\lap4all\Desktop\New folder\app.py"
if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"File length: {len(content)}")
    
    # Search for summary-dashboard, trends-dashboard, matrix-tables, opr, etc.
    keywords = ['summary-dashboard', 'trends-dashboard', 'matrix-tables', 'opr']
    for kw in keywords:
        idx = content.find(kw)
        if idx != -1:
            print(f"Keyword '{kw}' found at index {idx}, snippet: {content[idx-50:idx+150]}")
        else:
            print(f"Keyword '{kw}' NOT found")
else:
    print("app.py not found")

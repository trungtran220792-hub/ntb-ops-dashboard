# -*- coding: utf-8 -*-
import os

filepath = r"c:\Users\lap4all\Desktop\New folder\templates\index.html"
if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    keywords = ['loadNtbSummaryData', 'renderOprDashboard', 'setAmOprSort', 'renderNtbKpiCards', 'switchNtbRegion', 'matchNtbRegion']
    
    for kw in keywords:
        found = False
        for idx, line in enumerate(lines):
            if kw in line:
                print(f"Keyword '{kw}' found at line {idx+1}: {line.strip()[:120]}")
                found = True
        if not found:
            print(f"Keyword '{kw}' NOT found in templates/index.html")
else:
    print("templates/index.html not found")

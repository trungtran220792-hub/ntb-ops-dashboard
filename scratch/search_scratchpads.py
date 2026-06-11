# -*- coding: utf-8 -*-
import os

browser_dir = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\4336314d-71dd-4e55-8828-c64201e3d4a3\browser"
queries = ["renderNtbAnalysisTable", "setAmOprSort", "renderOprAmChartOnly", "tbody-ntb-ltc-analysis"]

if os.path.exists(browser_dir):
    files = os.listdir(browser_dir)
    print(f"Checking scratchpads in {browser_dir}:")
    for f in files:
        if f.startswith("scratchpad_") and f.endswith(".md"):
            path = os.path.join(browser_dir, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            for q in queries:
                if q in content:
                    print(f"  Found '{q}' in {f}!")
                    # print 500 characters around the query
                    idx = content.find(q)
                    print(content[max(0, idx-100):min(len(content), idx+500)])
                    print("-----------------------------")
else:
    print("Browser dir not found")

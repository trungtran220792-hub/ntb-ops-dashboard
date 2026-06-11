# -*- coding: utf-8 -*-
import os

brain_dir = r"C:\Users\lap4all\.gemini\antigravity-ide\brain"
queries = ["renderNtbAnalysisTable", "setAmOprSort", "renderOprAmChartOnly", "tbody-ntb-ltc-analysis"]

for root, dirs, files in os.walk(brain_dir):
    for f in files:
        if "scratchpad" in f.lower() and f.endswith(".md"):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
            except Exception:
                continue
            for q in queries:
                if q in content:
                    print(f"Found '{q}' in {os.path.relpath(path, brain_dir)}!")
                    idx = content.find(q)
                    print(content[max(0, idx-100):min(len(content), idx+500)])
                    print("-----------------------------")
print("Search complete.")

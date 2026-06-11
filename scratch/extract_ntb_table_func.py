# -*- coding: utf-8 -*-
import os

scratch_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"
path = os.path.join(scratch_dir, "extracted_ntb_js_from_summary.txt")

with open(path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Let's search for "function renderNtbAnalysisTable" and extract chunks
import re

matches = [m.start() for m in re.finditer("function renderNtbAnalysisTable", content)]
print("Found matches at:", matches)

for count, idx in enumerate(matches):
    snippet = content[idx:idx+8000]
    out_path = os.path.join(scratch_dir, f"recovered_table_func_{count}.js")
    with open(out_path, "w", encoding="utf-8") as out_f:
        out_f.write(snippet)
    print(f"Saved match {count} (length {len(snippet)}) to recovered_table_func_{count}.js")

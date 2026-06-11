# -*- coding: utf-8 -*-
import os

scratch_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"
path = os.path.join(scratch_dir, "script_opr_funcs.txt")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

print("File size:", len(content))

# Look for functions in script_opr_funcs.txt
idx = content.find("function renderNtbAnalysisTable")
if idx != -1:
    print("Found renderNtbAnalysisTable at index:", idx)
    # Print lines
    snippet = content[idx:]
    with open(os.path.join(scratch_dir, "recovered_ntb_funcs.js"), "w", encoding="utf-8") as f_out:
        f_out.write(snippet)
    print("Saved snippet of script_opr_funcs.txt from renderNtbAnalysisTable to recovered_ntb_funcs.js")
else:
    print("renderNtbAnalysisTable NOT found")

# -*- coding: utf-8 -*-
import os

filepath = r"c:\Users\lap4all\Desktop\New folder\scratch\past_ntb_funcs_found.txt"
if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Search for "renderNtbAnalysisTable"
    idx = 0
    while True:
        idx = content.find("renderNtbAnalysisTable", idx)
        if idx == -1:
            break
        print(f"Found renderNtbAnalysisTable in past_ntb_funcs_found.txt at index {idx}")
        print(content[idx:idx+500])
        print("-----------------------------------------")
        idx += 22 # move past keyword
else:
    print("past_ntb_funcs_found.txt not found")

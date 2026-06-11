# -*- coding: utf-8 -*-
import sys
import os

filepath = r"c:\Users\lap4all\Desktop\New folder\scratch\past_ntb_funcs_found.txt"
outpath = r"c:\Users\lap4all\Desktop\New folder\scratch\ntb_code.txt"

if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to find the section containing renderNtbAnalysisTable and extract the whole block
    idx = content.find("function renderNtbAnalysisTable")
    if idx != -1:
        # Let's extract 15000 characters from there to see the code of all these helper functions
        extracted = content[idx:idx+25000]
        with open(outpath, 'w', encoding='utf-8') as f_out:
            f_out.write(extracted)
        print("Successfully extracted renderNtbAnalysisTable and subsequent characters to ntb_code.txt")
    else:
        print("function renderNtbAnalysisTable not found")
else:
    print("past_ntb_funcs_found.txt not found")

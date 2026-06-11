# -*- coding: utf-8 -*-
import sys
import os

filepath = r"c:\Users\lap4all\Desktop\New folder\scratch\extracted_full_index_changes.txt"
outpath = r"c:\Users\lap4all\Desktop\New folder\scratch\index_changes_ntb.txt"

if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    idx = content.find("function renderNtbAnalysisTable")
    if idx != -1:
        extracted = content[idx:idx+35000]
        with open(outpath, 'w', encoding='utf-8') as f_out:
            f_out.write(extracted)
        print("Successfully extracted renderNtbAnalysisTable from extracted_full_index_changes.txt")
    else:
        print("function renderNtbAnalysisTable not found in extracted_full_index_changes.txt")
else:
    print("extracted_full_index_changes.txt not found")

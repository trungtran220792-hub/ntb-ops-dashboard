# -*- coding: utf-8 -*-
import os

filepath = r"c:\Users\lap4all\Desktop\New folder\scratch\index_changes_ntb.txt"
outpath = r"c:\Users\lap4all\Desktop\New folder\scratch\index_changes_ntb_formatted.txt"

if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the escaped \n with actual newlines, and also \t, \" etc.
    formatted = content.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"')
    
    with open(outpath, 'w', encoding='utf-8') as f_out:
        f_out.write(formatted)
    print("Formatted file written to index_changes_ntb_formatted.txt")
else:
    print("index_changes_ntb.txt not found")

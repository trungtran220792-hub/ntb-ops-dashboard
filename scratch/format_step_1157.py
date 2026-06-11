# -*- coding: utf-8 -*-
import os

filepath = r"c:\Users\lap4all\Desktop\New folder\scratch\step_1157_extracted.txt"
outpath = r"c:\Users\lap4all\Desktop\New folder\scratch\step_1157_formatted.txt"

if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    formatted = content.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"')
    
    with open(outpath, 'w', encoding='utf-8') as f_out:
        f_out.write(formatted)
    print("Formatted step_1157 saved to step_1157_formatted.txt")
else:
    print("step_1157_extracted.txt not found")

# -*- coding: utf-8 -*-
import os

filepath = r"c:\Users\lap4all\Desktop\New folder\scratch\extracted_steps\step_1157.txt"
outpath = r"c:\Users\lap4all\Desktop\New folder\scratch\step_1157_extracted.txt"

if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    idx = content.find("updateMetricCardUI")
    if idx != -1:
        extracted = content[idx:idx+4000]
        with open(outpath, 'w', encoding='utf-8') as out_f:
            out_f.write(extracted)
        print("Successfully extracted updateMetricCardUI to step_1157_extracted.txt")
    else:
        print("updateMetricCardUI not found")
else:
    print("step_1157.txt not found")

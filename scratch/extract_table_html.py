# -*- coding: utf-8 -*-
import os

filepath = r"c:\Users\lap4all\Desktop\New folder\scratch\steps_detail_summary.txt"
outpath = r"c:\Users\lap4all\Desktop\New folder\scratch\extracted_table_html.txt"

if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open(outpath, 'w', encoding='utf-8') as out_f:
        # Let's search for Step 1127
        idx_1127 = content.find("STEP 1127")
        if idx_1127 != -1:
            out_f.write("=== STEP 1127 CONTENT ===\n")
            out_f.write(content[idx_1127:idx_1127+8000].replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"'))
            out_f.write("\n\n" + "="*80 + "\n\n")
        
        # Let's search for Step 1131
        idx_1131 = content.find("STEP 1131")
        if idx_1131 != -1:
            out_f.write("=== STEP 1131 CONTENT ===\n")
            out_f.write(content[idx_1131:idx_1131+8000].replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"'))
            out_f.write("\n\n" + "="*80 + "\n\n")
            
        # Let's search for Step 1449
        idx_1449 = content.find("STEP 1449")
        if idx_1449 != -1:
            out_f.write("=== STEP 1449 CONTENT ===\n")
            out_f.write(content[idx_1449:idx_1449+8000].replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"'))
            out_f.write("\n\n" + "="*80 + "\n\n")
            
    print("Table HTML extracted to extracted_table_html.txt")
else:
    print("steps_detail_summary.txt not found")

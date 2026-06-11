# -*- coding: utf-8 -*-
import os

base_path = r"c:\Users\lap4all\Desktop\New folder\scratch\index.html.base"
out_path = r"c:\Users\lap4all\Desktop\New folder\scratch\index_base_utf8.html"
res_path = r"c:\Users\lap4all\Desktop\New folder\scratch\search_utf16_base_results.txt"

if os.path.exists(base_path):
    try:
        with open(base_path, 'r', encoding='utf-16') as f:
            content = f.read()
        
        # Write as UTF-8
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        with open(res_path, 'w', encoding='utf-8') as res:
            res.write(f"Reading {base_path} as UTF-16...\n")
            res.write(f"Successfully read {len(content)} characters.\n")
            res.write(f"Saved UTF-8 copy to {out_path}\n\n")
            
            keywords = ["nhân sự", "quản lý nhân sự", "gán tất cả", "gán tts", "odr tts", "tổng quan"]
            for kw in keywords:
                count = content.lower().count(kw)
                res.write(f"Keyword '{kw}': found {count} occurrences\n")
                
            # Let's search for some lines containing "Nhân sự" or "nhan-su"
            lines = content.split('\n')
            res.write("\nLines containing 'Nhân sự' or 'nhan-su' or 'nhan_su':\n")
            for i, line in enumerate(lines):
                if any(k in line.lower() for k in ["nhân sự", "nhan-su", "nhan_su"]):
                    res.write(f"Line {i+1}: {line.strip()}\n")
                    
    except Exception as e:
        with open(res_path, 'w', encoding='utf-8') as res:
            res.write(f"Error: {e}\n")
else:
    print(f"{base_path} not found")

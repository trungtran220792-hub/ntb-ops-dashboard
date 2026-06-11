import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\lap4all\Desktop\New folder\templates\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

keys = ["lam_dong", "binh_thuan", "khanh_hoa", "ninh_thuan", "dak_nong"]
for key in keys:
    print(f"Occurrences of '{key}':")
    for idx, line in enumerate(content.splitlines()):
        if key in line:
            print(f"  Line {idx+1}: {line.strip()}")

import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\lap4all\Desktop\New folder\app.py', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# find functions or variables related to province / prov / clean_str_key
for idx, line in enumerate(content.splitlines()):
    if 'clean_str_key' in line or 'mapped_prov' in line:
        print(f"Line {idx+1}: {line.strip()}")

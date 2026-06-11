import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\lap4all\Desktop\New folder\app.py', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for idx in range(2800, 2900):
    if idx < len(lines):
        print(f"{idx+1}: {lines[idx].rstrip()}")

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\lap4all\Desktop\New folder\templates\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for idx in range(2320, 2405):
    if idx < len(lines):
        print(f"{idx+1}: {lines[idx].rstrip()}")

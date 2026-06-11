import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\lap4all\Desktop\New folder\templates\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Let's search for matches of ltc-comp-1-val, comp-1-val, comp-2-val etc.
lines = content.splitlines()
for idx, line in enumerate(lines):
    if 'comp-1-val' in line or 'comp-2-val' in line or 'comp-1-diff' in line or 'comp-2-diff' in line:
        print(f"Line {idx+1}: {line.strip()}")

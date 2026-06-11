import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\lap4all\Desktop\New folder\app.py', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Let's search for "mapped_am" in app.py
lines = content.splitlines()
for idx, line in enumerate(lines):
    if 'mapped_am' in line:
        print(f"Line {idx+1}: {line.strip()}")

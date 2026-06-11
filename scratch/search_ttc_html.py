import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\lap4all\Desktop\New folder\templates\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Let's search for "TTC" in index.html (case sensitive)
lines = content.splitlines()
for idx, line in enumerate(lines):
    if 'TTC' in line:
        if idx > 2000 and idx < 6500: # around the NTB summary section
            print(f"Line {idx+1}: {line.strip()}")

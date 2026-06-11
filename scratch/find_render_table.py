import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\lap4all\Desktop\New folder\templates\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Let's search for "function renderNtbAnalysisTable"
lines = content.splitlines()
start = -1
for idx, line in enumerate(lines):
    if 'function renderNtbAnalysisTable' in line:
        start = idx
        break

if start != -1:
    print(f"Found renderNtbAnalysisTable at line {start+1}")
    for i in range(start, min(len(lines), start + 100)):
        print(f"{i+1}: {lines[i]}")
else:
    print("Function renderNtbAnalysisTable not found")

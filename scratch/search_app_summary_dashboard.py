import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
found = False
for idx, line in enumerate(lines):
    if '/api/summary-dashboard' in line:
        found = True
        print(f"Line {idx+1}: {line.strip()}")
        # print subsequent lines
        for j in range(idx+1, min(len(lines), idx+60)):
            print(f"  Line {j+1}: {lines[j].strip()}")
        break

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\lap4all\Desktop\New folder\templates\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'function renderNtbKpiCards(' in line:
        print(f"Line {idx+1}: {line.strip()}")
        # print next 120 lines
        for i in range(idx, min(len(lines), idx + 120)):
            print(f"  {i+1}: {lines[i].rstrip()}")
        break

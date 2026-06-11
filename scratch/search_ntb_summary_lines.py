with open(r'c:\Users\lap4all\Desktop\New folder\templates\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'ntb-kpi-card' in line or 'tab-ntb-summary' in line:
        print(f"Line {idx+1}: {line.strip()}")

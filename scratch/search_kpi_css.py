with open(r'c:\Users\lap4all\Desktop\New folder\templates\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'kpi-grid' in line or 'kpi-card' in line:
        if 'grid' in line or 'display:' in line or 'width:' in line or '{' in line:
            print(f"Line {idx+1}: {line.strip()}")

with open(r'c:\Users\lap4all\Desktop\New folder\templates\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

in_ntb = False
for idx, line in enumerate(lines):
    if 'id="tab-ntb-summary"' in line:
        in_ntb = True
    if in_ntb and 'class="card"' in line and idx > 2300:
        # We want to print lines around this tab
        pass
    if in_ntb and 'ntb-kpi-card' in line:
        print(f"Line {idx+1}: {line.strip()}")
        # print next 25 lines
        for i in range(idx, min(len(lines), idx + 25)):
            print(f"  {i+1}: {lines[i].strip()}")
        print("-" * 40)

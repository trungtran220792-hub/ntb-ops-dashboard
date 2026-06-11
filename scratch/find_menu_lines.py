import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('templates/index.html', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if 'tab-dashboard' in line or 'tab-introduction' in line or 'Giới thiệu NTB' in line or 'Tổng quan' in line:
            if 'class=' in line or 'onclick' in line or 'id=' in line:
                print(f"Line {i}: {line.strip()}")

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('templates/index.html', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if 'function switchTab' in line or 'switchTab(' in line:
            print(f"Line {i}: {line.strip()}")

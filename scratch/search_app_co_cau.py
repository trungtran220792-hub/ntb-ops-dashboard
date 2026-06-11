import sys
sys.path.append('.')

sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if 'co_cau' in line.lower() or 'cơ cấu' in line.lower() or 'merge' in line.lower():
            print(f"Line {idx+1}: {line.strip()}")

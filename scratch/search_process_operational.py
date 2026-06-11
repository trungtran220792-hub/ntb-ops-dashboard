import sys
sys.path.append('.')

sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if 'process_operational_report' in line:
            print(f"Line {idx+1}: {line.strip()}")

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if '/api/operational' in line or 'operational_cache' in line.lower() or '/api/opr' in line:
            print(f"Line {idx+1}: {line.strip()}")

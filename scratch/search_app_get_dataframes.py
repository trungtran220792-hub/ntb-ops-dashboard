import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if 'get_dataframes' in line:
            print(f"Line {i}: {line.strip()}")

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if "['Tỉnh']" in line or "['AM']" in line:
            # exclude lines that are in get_dataframes or configuration
            if idx+1 not in [1704, 1705, 415, 416, 1626, 1625]:
                print(f"Line {idx+1}: {line.strip()}")

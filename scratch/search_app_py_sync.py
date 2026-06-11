with open('app.py', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if 'sync' in line.lower() or 'download' in line.lower():
            print(f"Line {idx+1}: {line.strip()}")

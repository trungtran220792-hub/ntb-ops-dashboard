import sys
sys.path.append('.')

sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if 'global ' in line or '_cache' in line.lower() or 'cache_lock' in line.lower() or 'operational_cache' in line.lower():
            if idx < 600: # print first occurrences
                print(f"Line {idx+1}: {line.strip()}")

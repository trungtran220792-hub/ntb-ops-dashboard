import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if 'odr' in line.lower() or 'tts' in line.lower():
            if idx < 1000 or 'odr' in line.lower():
                print(f"Line {idx+1}: {line.strip()}")

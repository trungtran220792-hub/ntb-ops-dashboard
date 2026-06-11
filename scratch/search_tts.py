import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'c:\Users\lap4all\Desktop\New folder\app.py', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

for idx, line in enumerate(content.splitlines()):
    if 'tts' in line.lower():
        print(f"Line {idx+1}: {line.strip()}")

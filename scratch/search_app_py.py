import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\lap4all\Desktop\New folder\app.py', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

print("All lines with @app.route:")
for idx, line in enumerate(lines):
    if '@app.route' in line:
        print(f"Line {idx+1}: {line.strip()}")
        # print subsequent lines until def
        for i in range(idx + 1, min(len(lines), idx + 5)):
            print(f"  Line {i+1}: {lines[i].strip()}")
            if 'def ' in lines[i]:
                break

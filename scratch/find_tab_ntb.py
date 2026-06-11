import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\lap4all\Desktop\New folder\templates\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Let's search for "Target: \u2265" or "% LTC" in index.html
lines = content.splitlines()
for idx, line in enumerate(lines):
    if '% LTC' in line or 'Target:' in line:
        if idx > 2000 and idx < 4500: # around the NTB summary section
            print(f"Line {idx+1}: {line.strip()}")
            # print surrounding 10 lines
            for i in range(max(0, idx-2), min(len(lines), idx+15)):
                print(f"  {i+1}: {lines[i]}")
            print("-" * 50)

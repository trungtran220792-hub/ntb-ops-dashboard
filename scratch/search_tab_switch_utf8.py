import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\lap4all\Desktop\New folder\templates\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer('switchTab', content)]
print(f"Found {len(matches)} occurrences of switchTab")
for m in matches:
    start = max(0, m - 100)
    end = min(len(content), m + 150)
    snippet = content[start:end]
    if 'function ' in snippet or 'window' in snippet or 'onload' in snippet or 'document.' in snippet or 'active' in snippet:
        print(f"--- MATCH ---")
        print(snippet)
        print("-" * 50)

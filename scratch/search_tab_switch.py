with open(r'c:\Users\lap4all\Desktop\New folder\templates\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer('switchTab', content)]
print(f"Found {len(matches)} occurrences of switchTab")
for m in matches[:10]:
    start = max(0, m - 50)
    end = min(len(content), m + 100)
    print(f"Around: {repr(content[start:end])}\n")

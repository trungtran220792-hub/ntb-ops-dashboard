import re

with open(r'c:\Users\lap4all\Desktop\New folder\templates\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("Searching for OPR section and chart rendering...")

lines = content.splitlines()
results = []
for i, line in enumerate(lines):
    line_lower = line.lower()
    if any(k in line_lower for k in ['opr', 'xếp hạng', 'hiệu suất', 'sort', 'apex', 'chart', 'sắp xếp', 'thấp', 'cao']):
        results.append(f"L{i+1}: {line.strip()}")

with open(r'c:\Users\lap4all\Desktop\New folder\scratch\search_opr_res.txt', 'w', encoding='utf-8') as f_out:
    for res in results:
        f_out.write(res + "\n")

print(f"Done. Found {len(results)} matches.")

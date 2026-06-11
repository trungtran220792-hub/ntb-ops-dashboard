with open(r'c:\Users\lap4all\Desktop\New folder\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
results = []
for i, line in enumerate(lines):
    if 'co_cau_ntb.xlsx' in line or 'co_cau_ntb' in line:
        results.append(f"L{i+1}: {line.strip()}")

with open(r'c:\Users\lap4all\Desktop\New folder\scratch\co_cau_refs.txt', 'w', encoding='utf-8') as f_out:
    for res in results:
        f_out.write(res + "\n")

print(f"Done. Found {len(results)} occurrences in app.py.")

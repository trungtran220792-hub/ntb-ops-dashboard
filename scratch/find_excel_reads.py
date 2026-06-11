with open(r'c:\Users\lap4all\Desktop\New folder\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
results = []
for i, line in enumerate(lines):
    if 'read_excel' in line or 'load_sheet_cached' in line or 'ExcelFile' in line:
        results.append(f"L{i+1}: {line.strip()}")

with open(r'c:\Users\lap4all\Desktop\New folder\scratch\excel_reads.txt', 'w', encoding='utf-8') as f_out:
    for res in results:
        f_out.write(res + "\n")

print(f"Done. Found {len(results)} occurrences.")

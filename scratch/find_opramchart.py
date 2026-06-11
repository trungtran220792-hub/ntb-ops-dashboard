with open(r'c:\Users\lap4all\Desktop\New folder\templates\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
results = []
for i, line in enumerate(lines):
    if 'oprAmChart' in line:
        results.append(f"L{i+1}: {line.strip()}")

with open(r'c:\Users\lap4all\Desktop\New folder\scratch\opramchart_occurrences.txt', 'w', encoding='utf-8') as f_out:
    for res in results:
        f_out.write(res + "\n")

print(f"Done. Found {len(results)} occurrences of oprAmChart.")

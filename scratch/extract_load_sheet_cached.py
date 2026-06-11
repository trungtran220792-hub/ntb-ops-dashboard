with open(r'c:\Users\lap4all\Desktop\New folder\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
results = []
found = False
for i, line in enumerate(lines):
    if 'def load_sheet_cached' in line:
        results.append((i+1, line))
        for j in range(1, 40):
            if i + j < len(lines):
                results.append((i+j+1, lines[i+j]))
        found = True
        break

if found:
    with open(r'c:\Users\lap4all\Desktop\New folder\scratch\load_sheet_cached_def.txt', 'w', encoding='utf-8') as f_out:
        for idx, line in results:
            f_out.write(f"L{idx}: {line}\n")
    print("Extracted load_sheet_cached to scratch/load_sheet_cached_def.txt")
else:
    print("def load_sheet_cached not found")

with open(r'c:\Users\lap4all\Desktop\New folder\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
results = []
found = False
for i, line in enumerate(lines):
    if 'Auto-update co_cau_ntb.xlsx' in line:
        results.append((i+1, line))
        for j in range(1, 40):
            if i + j < len(lines):
                results.append((i+j+1, lines[i+j]))
        found = True
        break

if found:
    with open(r'c:\Users\lap4all\Desktop\New folder\scratch\co_cau_update_def.txt', 'w', encoding='utf-8') as f_out:
        for idx, line in results:
            f_out.write(f"L{idx}: {line}\n")
    print("Extracted co_cau update to scratch/co_cau_update_def.txt")
else:
    print("Auto-update co_cau_ntb.xlsx not found")

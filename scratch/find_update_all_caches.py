with open(r'c:\Users\lap4all\Desktop\New folder\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
results = []
found = False
for i, line in enumerate(lines):
    if 'def update_all_caches' in line:
        results.append((i+1, line))
        for j in range(1, 100):
            if i + j < len(lines):
                results.append((i+j+1, lines[i+j]))
        found = True
        break

if found:
    with open(r'c:\Users\lap4all\Desktop\New folder\scratch\update_all_caches_def.txt', 'w', encoding='utf-8') as f_out:
        for idx, line in results:
            f_out.write(f"L{idx}: {line}\n")
    print("Extracted update_all_caches to scratch/update_all_caches_def.txt")
else:
    print("def update_all_caches not found")

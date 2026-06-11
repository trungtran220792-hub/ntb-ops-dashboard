with open(r'c:\Users\lap4all\Desktop\New folder\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
results = []
for i, line in enumerate(lines):
    if '@app.route' in line and ('sync' in line.lower() or 'download' in line.lower()):
        results.append((i+1, line))
        for j in range(1, 100):
            if i + j < len(lines):
                results.append((i+j+1, lines[i+j]))
        break

if results:
    with open(r'c:\Users\lap4all\Desktop\New folder\scratch\sync_route_def.txt', 'w', encoding='utf-8') as f_out:
        for idx, line in results:
            f_out.write(f"L{idx}: {line}\n")
    print(f"Extracted sync route to scratch/sync_route_def.txt. Count: {len(results)} lines.")
else:
    print("No sync route found.")

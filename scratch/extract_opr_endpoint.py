with open(r'c:\Users\lap4all\Desktop\New folder\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
results = []
for i, line in enumerate(lines):
    if '@app.route' in line and 'opr' in line.lower():
        results.append((i+1, line))
        # Print next 60 lines
        for j in range(1, 120):
            if i + j < len(lines):
                results.append((i+j+1, lines[i+j]))

with open(r'c:\Users\lap4all\Desktop\New folder\scratch\opr_endpoint.txt', 'w', encoding='utf-8') as f_out:
    for idx, line in results:
        f_out.write(f"L{idx}: {line}\n")

print(f"Extracted OPR endpoint context to scratch/opr_endpoint.txt. Count: {len(results)} lines.")

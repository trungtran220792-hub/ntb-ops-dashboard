with open(r'c:\Users\lap4all\Desktop\New folder\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
results = []
found = False
for i, line in enumerate(lines):
    if 'load_vols_tao_don_df' in line or 'vols_tao_don' in line:
        results.append((i+1, line))
        for j in range(1, 40):
            if i + j < len(lines):
                results.append((i+j+1, lines[i+j]))
        found = True
        break

if found:
    with open(r'c:\Users\lap4all\Desktop\New folder\scratch\vols_tao_don_def.txt', 'w', encoding='utf-8') as f_out:
        for idx, line in results:
            f_out.write(f"L{idx}: {line}\n")
    print("Extracted vols_tao_don loader to scratch/vols_tao_don_def.txt")
else:
    print("load_vols_tao_don_df not found")

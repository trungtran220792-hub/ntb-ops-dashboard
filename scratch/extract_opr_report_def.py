with open(r'c:\Users\lap4all\Desktop\New folder\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
results = []
found = False
for i, line in enumerate(lines):
    if 'def process_opr_report' in line:
        results.append((i+1, line))
        # Print next 200 lines
        for j in range(1, 200):
            if i + j < len(lines):
                results.append((i+j+1, lines[i+j]))
        found = True
        break

if found:
    with open(r'c:\Users\lap4all\Desktop\New folder\scratch\opr_report_def.txt', 'w', encoding='utf-8') as f_out:
        for idx, line in results:
            f_out.write(f"L{idx}: {line}\n")
    print(f"Extracted process_opr_report to scratch/opr_report_def.txt. Count: {len(results)} lines.")
else:
    print("def process_opr_report not found")

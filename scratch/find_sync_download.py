with open(r'c:\Users\lap4all\Desktop\New folder\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
results = []
for i, line in enumerate(lines):
    if 'def download' in line or 'def sync' in line or 'gspread' in line or 'google' in line.lower() or 'import urllib' in line or 'requests.get' in line:
        results.append((i+1, line))
        for j in range(1, 40):
            if i + j < len(lines):
                results.append((i+j+1, lines[i+j]))
        break

if results:
    with open(r'c:\Users\lap4all\Desktop\New folder\scratch\sync_download_def.txt', 'w', encoding='utf-8') as f_out:
        for idx, line in results:
            f_out.write(f"L{idx}: {line}\n")
    print("Extracted sync/download context to scratch/sync_download_def.txt")
else:
    print("No sync/download functions found.")

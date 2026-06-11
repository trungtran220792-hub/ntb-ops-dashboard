import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\lap4all\Desktop\New folder\templates\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Let's search for "Số đơn chưa hoàn thành" or "backlog" in templates/index.html
lines = content.splitlines()
for idx, line in enumerate(lines):
    if 'chưa hoàn thành' in line or 'chart-backlog' in line or 'backlog' in line.lower():
        if idx > 1500 and idx < 4000:
            print(f"Line {idx+1}: {line.strip()}")

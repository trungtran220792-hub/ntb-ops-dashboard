import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\lap4all\Desktop\New folder\templates\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Let's search for chart-ntb-backlog-am or backlog related chart variables
lines = content.splitlines()
for idx, line in enumerate(lines):
    if 'chart-ntb-backlog-am' in line or 'ntbBacklogChart' in line or 'ntb_backlog' in line.lower():
        print(f"Line {idx+1}: {line.strip()}")

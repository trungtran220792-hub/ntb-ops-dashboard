import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\lap4all\Desktop\New folder\templates\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Let's search for table headers of table-ntb-ltc-analysis and table-ntb-gtc-analysis
lines = content.splitlines()
for idx, line in enumerate(lines):
    if 'table-ntb-ltc-analysis' in line or 'table-ntb-gtc-analysis' in line:
        print(f"Line {idx+1}: {line.strip()}")
        # print next 25 lines
        for i in range(idx, min(len(lines), idx + 25)):
            print(f"  {i+1}: {lines[i]}")

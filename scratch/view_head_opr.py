import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
head_content = subprocess.check_output(['git', 'show', 'HEAD:app.py']).decode('utf-8', errors='ignore')
lines = head_content.splitlines()

start = None
end = None
for idx, line in enumerate(lines, 1):
    if 'def process_opr_report' in line:
        start = idx
    if start is not None and line.startswith('def ') and idx > start:
        end = idx
        break

if start is not None:
    if end is None:
        end = len(lines)
    for idx in range(start - 1, end - 1):
        print(f"{idx+1}: {lines[idx]}")

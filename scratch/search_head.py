import subprocess

head_content = subprocess.check_output(['git', 'show', 'HEAD:app.py']).decode('utf-8', errors='ignore')
lines = head_content.splitlines()

print("Searching for OPR raw files or filtering...")
for idx, line in enumerate(lines, 1):
    if 'opr' in line.lower() or 'oe' in line.lower():
        if 'read' in line or 'filter' in line or 'csv' in line:
            print(f"{idx}: {line.strip()}")

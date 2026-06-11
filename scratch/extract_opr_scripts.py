import re

with open(r'c:\Users\lap4all\Desktop\New folder\templates\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for script tags or function definitions related to OPR dashboard
results = []
lines = content.splitlines()

in_script = False
script_lines = []
for i, line in enumerate(lines):
    if '<script' in line:
        in_script = True
    if in_script:
        script_lines.append((i+1, line))
    if '</script>' in line:
        in_script = False

print(f"Total script lines: {len(script_lines)}")

# Let's find functions inside scripts
func_pattern = re.compile(r'(function\s+\w+|const\s+\w+\s*=\s*(async\s*)?\([^)]*\)\s*=>|\w+\s*\([^)]*\)\s*\{)')
opr_funcs = []
for idx, line in script_lines:
    if 'function' in line or '=>' in line or 'opr' in line.lower() or 'chart' in line.lower() or 'sort' in line.lower():
        if any(keyword in line.lower() for keyword in ['opr', 'chart', 'sort', 'render', 'update', 'rank']):
            opr_funcs.append(f"L{idx}: {line.strip()}")

with open(r'c:\Users\lap4all\Desktop\New folder\scratch\script_opr_funcs.txt', 'w', encoding='utf-8') as f_out:
    for f_line in opr_funcs:
        f_out.write(f_line + "\n")

print(f"Done. Found {len(opr_funcs)} matching script lines.")

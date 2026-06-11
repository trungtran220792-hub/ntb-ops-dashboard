import subprocess
import re

# Get functions/routes from current app.py
routes_current = []
funcs_current = []
with open('app.py', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        if line.strip().startswith('@app.route'):
            routes_current.append((idx, line.strip()))
        elif line.strip().startswith('def '):
            funcs_current.append((idx, line.strip()))

# Get functions/routes from HEAD:app.py
head_content = subprocess.check_output(['git', 'show', 'HEAD:app.py']).decode('utf-8', errors='ignore')
routes_head = []
funcs_head = []
for idx, line in enumerate(head_content.splitlines(), 1):
    if line.strip().startswith('@app.route'):
        routes_head.append((idx, line.strip()))
    elif line.strip().startswith('def '):
        funcs_head.append((idx, line.strip()))

print("=== ROUTES IN HEAD BUT NOT IN CURRENT ===")
current_route_names = [r[1] for r in routes_current]
for idx, r in routes_head:
    if r not in current_route_names:
        print(f"HEAD Line {idx}: {r}")

print("\n=== FUNCTIONS IN HEAD BUT NOT IN CURRENT ===")
current_func_names = [f[1] for f in funcs_current]
for idx, f in funcs_head:
    # Compare raw function signature
    sig = f.split('(')[0]
    curr_sigs = [cf.split('(')[0] for cf in current_func_names]
    if sig not in curr_sigs:
        print(f"HEAD Line {idx}: {f}")

print("\n=== ROUTES IN CURRENT BUT NOT IN HEAD ===")
head_route_names = [r[1] for r in routes_head]
for idx, r in routes_current:
    if r not in head_route_names:
        print(f"Current Line {idx}: {r}")

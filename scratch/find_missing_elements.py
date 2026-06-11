import re

# Extract tabs/menu items from index.html.base
print("=== TABS IN index.html.base ===")
tabs_base = []
with open('scratch/index.html.base', 'r', encoding='utf-16') as f:
    for idx, line in enumerate(f, 1):
        if 'switchTab' in line and ('menu-item' in line or 'onclick' in line):
            print(f"Base Line {idx}: {line.strip()}")
            tabs_base.append(line.strip())

# Extract tabs/menu items from current templates/index.html
print("\n=== TABS IN current templates/index.html ===")
tabs_curr = []
with open('templates/index.html', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        if 'switchTab' in line and ('menu-item' in line or 'onclick' in line):
            print(f"Current Line {idx}: {line.strip()}")
            tabs_curr.append(line.strip())

# Compare routes in app.py.base vs current app.py
print("\n=== ROUTES IN app.py.base ===")
routes_base = []
with open('scratch/app.py.base', 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f, 1):
        if '@app.route' in line:
            routes_base.append(line.strip())
print(f"Found {len(routes_base)} routes in app.py.base")

routes_curr = []
with open('app.py', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        if '@app.route' in line:
            routes_curr.append(line.strip())
print(f"Found {len(routes_curr)} routes in current app.py")

print("\n=== ROUTES IN BASE BUT NOT IN CURRENT ===")
for r in routes_base:
    if r not in routes_curr:
        print(r)

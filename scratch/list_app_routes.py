import re

app_path = r"c:\Users\lap4all\Desktop\New folder\app.py"
routes = []

with open(app_path, 'r', encoding='utf-8') as f:
    for line_num, line in enumerate(f, 1):
        if "@app.route" in line:
            routes.append((line_num, line.strip()))

print(f"Found {len(routes)} routes in app.py:")
for num, route in routes:
    print(f"Line {num}: {route}")

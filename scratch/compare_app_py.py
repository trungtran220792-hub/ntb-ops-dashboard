import re

def parse_endpoints(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Let's find Flask routes, typically @app.route(...)
    routes = re.findall(r'@app\.route\([\'"]([^\'"]+)[\'"](?:,\s*methods=\[([^\]]+)\])?\)', content)
    route_details = []
    for r in routes:
        route_details.append(f"  {r[0]} ({r[1] if r[1] else 'GET'})")
    return route_details

curr_routes = parse_endpoints("c:/Users/lap4all/Desktop/New folder/app.py")
back_routes = parse_endpoints("c:/Users/lap4all/Desktop/New folder/scratch/app_backup_before_reset.py")

print("=== Routes in active app.py ===")
for r in curr_routes:
    print(r)

print("\n=== Routes in backup app_backup_before_reset.py ===")
for r in back_routes:
    print(r)

print("\n=== Route differences ===")
print("In backup but NOT in current app.py:")
for r in back_routes:
    if r not in curr_routes:
        print(r)

print("\nIn current but NOT in backup app.py:")
for r in curr_routes:
    if r not in back_routes:
        print(r)

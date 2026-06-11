# -*- coding: utf-8 -*-
import os

filepath = r"c:\Users\lap4all\Desktop\New folder\app.py"
out = open(r"c:\Users\lap4all\Desktop\New folder\scratch\app_routes_info.txt", "w", encoding="utf-8")

if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    routes = [
        "/api/summary-dashboard",
        "/api/opr",
        "/api/matrix-tables"
    ]
    
    for r in routes:
        idx = content.find(r)
        if idx == -1:
            out.write(f"Route {r} NOT FOUND in app.py\n\n")
            continue
        out.write(f"=========================================\n")
        out.write(f"ROUTE: {r} (found at index {idx})\n")
        out.write(f"=========================================\n")
        
        # print route definition (from def up to the next route or about 200 lines)
        start = max(0, content.rfind("@app.route", 0, idx))
        end = content.find("@app.route", idx + len(r))
        if end == -1:
            end = len(content)
        
        out.write(content[start:end])
        out.write("\n\n")
else:
    out.write("app.py not found\n")

out.close()
print("Saved route info to app_routes_info.txt")

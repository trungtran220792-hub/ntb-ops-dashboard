with open("c:/Users/lap4all/Desktop/New folder/app.py", "r", encoding="utf-8") as f:
    curr_content = f.read()

with open("c:/Users/lap4all/Desktop/New folder/scratch/app_backup_before_reset.py", "r", encoding="utf-8") as f:
    back_content = f.read()

def extract_route_function(content, route_path):
    import re
    # Find @app.route('/api/volume-creation' ...)
    pattern = rf'@app\.route\([\'"]{route_path}[\'"]'
    match = re.search(pattern, content)
    if not match:
        return f"Route {route_path} not found"
    
    start_pos = match.start()
    # Find def ... function name
    def_match = re.search(r'def\s+(\w+)\s*\([^)]*\)\s*:', content[start_pos:])
    if not def_match:
        return f"Function definition not found after route {route_path}"
    
    func_start = start_pos + def_match.start()
    # We want to find where the function ends. Usually indentation decreases back to 0.
    # Let's count indentation of the line after 'def ...:'
    lines = content[func_start:].splitlines()
    func_lines = [lines[0]]
    def_indent = len(lines[0]) - len(lines[0].lstrip())
    
    body_indent = None
    for line in lines[1:]:
        if not line.strip():
            func_lines.append(line)
            continue
        line_indent = len(line) - len(line.lstrip())
        if body_indent is None:
            body_indent = line_indent
        if line_indent <= def_indent:
            break
        func_lines.append(line)
    
    return "\n".join(func_lines)

curr_func = extract_route_function(curr_content, '/api/volume-creation')
back_func = extract_route_function(back_content, '/api/volume-creation')

print("=== CURRENT FUNCTION ===")
print(len(curr_func))
print("=== BACKUP FUNCTION ===")
print(len(back_func))

if curr_func == back_func:
    print("API implementation is IDENTICAL")
else:
    print("API implementation is DIFFERENT")
    with open("c:/Users/lap4all/Desktop/New folder/scratch/volume_api_curr.py", "w", encoding="utf-8") as f:
        f.write(curr_func)
    with open("c:/Users/lap4all/Desktop/New folder/scratch/volume_api_back.py", "w", encoding="utf-8") as f:
        f.write(back_func)
    print("Saved code to scratch/volume_api_curr.py and scratch/volume_api_back.py")

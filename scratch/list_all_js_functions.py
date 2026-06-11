# -*- coding: utf-8 -*-
import os
import re

files_to_check = [
    r"c:\Users\lap4all\Desktop\New folder\templates\index.html",
    r"c:\Users\lap4all\Desktop\New folder\scratch\render_index.html",
    r"c:\Users\lap4all\Desktop\New folder\scratch\index.html.base",
    r"c:\Users\lap4all\Desktop\New folder\scratch\index.html.patched"
]

out = open(r"c:\Users\lap4all\Desktop\New folder\scratch\list_functions_res.txt", "w", encoding="utf-8")

def get_content(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(path, 'r', encoding='utf-16') as f:
                return f.read()
        except:
            return None

for path in files_to_check:
    content = get_content(path)
    if content is None:
        out.write(f"File {path} - NOT FOUND or READ ERROR\n\n")
        continue
    
    out.write(f"=========================================\n")
    out.write(f"FILE: {path}\n")
    out.write(f"  Size: {os.path.getsize(path)} bytes\n")
    out.write(f"=========================================\n")
    
    # Extract function names
    funcs = re.findall(r"function\s+([a-zA-Z0-9_]+)\s*\(", content)
    out.write(f"  Functions found ({len(funcs)}):\n")
    for f in sorted(list(set(funcs))):
        out.write(f"    - {f}\n")
        
    # Extract IDs in content
    ids = re.findall(r'id=["\']([a-zA-Z0-9_-]+)["\']', content)
    out.write(f"  IDs found ({len(ids)}):\n")
    interesting_ids = [i for i in ids if 'ntb' in i.lower() or 'opr' in i.lower()]
    for i in sorted(list(set(interesting_ids))):
        out.write(f"    - {i}\n")
    out.write("\n")

out.close()
print("Saved functions list to list_functions_res.txt")

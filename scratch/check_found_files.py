# -*- coding: utf-8 -*-
import os

files = [
    r"c:\Users\lap4all\Desktop\New folder\scratch\script_opr_funcs.txt",
    r"c:\Users\lap4all\Desktop\New folder\scratch\past_ntb_funcs_found.txt"
]

out = open(r"c:\Users\lap4all\Desktop\New folder\scratch\found_files_inspect.txt", "w", encoding="utf-8")

for path in files:
    if os.path.exists(path):
        out.write(f"=========================================\n")
        out.write(f"FILE: {path}\n")
        out.write(f"  Size: {os.path.getsize(path)} bytes\n")
        out.write(f"=========================================\n")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # print some info about what's inside
        lines = content.splitlines()
        out.write(f"  Total lines: {len(lines)}\n")
        
        # print the first 50 lines and last 50 lines of script_opr_funcs.txt
        if "script_opr_funcs" in path:
            out.write("--- FIRST 100 LINES ---\n")
            out.write("\n".join(lines[:100]))
            out.write("\n...\n")
            out.write("--- LAST 100 LINES ---\n")
            out.write("\n".join(lines[-100:]))
        else:
            # past_ntb_funcs_found.txt is large, search for occurrences of function definitions
            for i, line in enumerate(lines, 1):
                if "function " in line or "class=" in line or "id=" in line:
                    if any(x in line for x in ["renderNtb", "switchNtb", "loadNtb", "setAmOpr", "renderOpr"]):
                        out.write(f"  Line {i}: {line[:120]}\n")
    else:
        out.write(f"File {path} does not exist\n")

out.close()
print("Saved inspection to found_files_inspect.txt")

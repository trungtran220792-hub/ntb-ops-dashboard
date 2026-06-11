with open("c:/Users/lap4all/Desktop/New folder/templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
funcs = ["loadGoogleSheetsConfig", "saveGoogleSheetsConfig"]
out = []
for func_name in funcs:
    pattern = rf'async\s+function\s+{func_name}\s*\([^)]*\)\s*\{{'
    match = re.search(pattern, content)
    if match:
        start_pos = match.start()
        open_brackets = 0
        pos = start_pos
        while pos < len(content):
            if content[pos] == '{':
                open_brackets += 1
            elif content[pos] == '}':
                open_brackets -= 1
                if open_brackets == 0:
                    out.append(f"=== {func_name} ===")
                    out.append(content[start_pos:pos+1])
                    break
            pos += 1

with open("c:/Users/lap4all/Desktop/New folder/scratch/config_js_code.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("Saved config functions to scratch/config_js_code.txt")

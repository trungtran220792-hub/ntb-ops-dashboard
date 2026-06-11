with open("c:/Users/lap4all/Desktop/New folder/templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
pattern = r'function\s+switchTab\s*\([^)]*\)\s*\{'
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
                with open("c:/Users/lap4all/Desktop/New folder/scratch/switch_tab_code.txt", "w", encoding="utf-8") as f:
                    f.write(content[start_pos:pos+1])
                print("Saved switchTab code to scratch/switch_tab_code.txt")
                break
        pos += 1
else:
    print("switchTab not found")

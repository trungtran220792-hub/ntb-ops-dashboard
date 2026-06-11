# -*- coding: utf-8 -*-
with open("templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Let's search for lines containing switchTab
with open(r"scratch\switch_tab_search.txt", "w", encoding="utf-8") as out:
    for idx, line in enumerate(content.splitlines()):
        if "switchTab" in line:
            out.write(f"Line {idx+1}: {line.strip()}\n")
print("Done")

# -*- coding: utf-8 -*-
with open("templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Let's find saveGoogleSheetsConfig and loadGoogleSheetsConfig
idx_load = content.find("function loadGoogleSheetsConfig")
idx_save = content.find("function saveGoogleSheetsConfig")

with open(r"scratch\sheets_config_js_inspect.txt", "w", encoding="utf-8") as out:
    if idx_load != -1:
        out.write("=== loadGoogleSheetsConfig ===\n")
        out.write(content[idx_load:idx_load+800])
        out.write("\n\n")
    if idx_save != -1:
        out.write("=== saveGoogleSheetsConfig ===\n")
        out.write(content[idx_save:idx_save+800])
        out.write("\n\n")

print("Done")

# -*- coding: utf-8 -*-
with open(r"scratch\diff_app_utf8.txt", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("def async_sync_task")
with open(r"scratch\sync_task_logic.txt", "w", encoding="utf-8") as out:
    if idx != -1:
        out.write(content[idx:idx+3000])
    else:
        out.write("Not found\n")
print("Done")

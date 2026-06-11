# -*- coding: utf-8 -*-
with open("templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find('id="tab-sync"')
with open(r"scratch\tab_sync_inspect.txt", "w", encoding="utf-8") as out:
    if idx != -1:
        out.write(content[idx:idx+1500])
    else:
        out.write("Not found\n")
print("Done")

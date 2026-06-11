# -*- coding: utf-8 -*-
with open(r"scratch\diff_app_utf8.txt", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("def process_operational_report")
with open(r"scratch\process_op_diff.txt", "w", encoding="utf-8") as out:
    if idx != -1:
        out.write(content[idx:idx+4000])
    else:
        out.write("Not found\n")
print("Done")

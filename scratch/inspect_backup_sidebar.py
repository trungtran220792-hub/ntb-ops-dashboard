# -*- coding: utf-8 -*-
import os

backup_path = r"c:\Users\lap4all\Desktop\New folder\scratch\templates_index_backup_before_reset.html"
with open(backup_path, "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("nav-tab-nhan-su")
with open(r"scratch\inspect_backup_sidebar_output.txt", "w", encoding="utf-8") as out:
    if idx != -1:
        out.write("=== Sidebar Menu in Backup ===\n")
        out.write(content[idx-200:idx+400])
    else:
        out.write("nav-tab-nhan-su not found\n")

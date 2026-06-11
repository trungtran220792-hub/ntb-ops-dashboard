# -*- coding: utf-8 -*-
import os
import time

scratch_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"
files = [
    "app.py.base", "app.py.patched", "diff_app.txt", "diff_app_current.txt", 
    "diff_app_utf8.txt", "index.html.base", "index.html.patched", 
    "git_diff_index.txt", "index_current_backup.html", "index_base_utf8.html"
]

for filename in files:
    path = os.path.join(scratch_dir, filename)
    if os.path.exists(path):
        mtime = os.path.getmtime(path)
        size = os.path.getsize(path)
        print(f"File {filename:30s} Size: {size:8d} bytes, Modified: {time.ctime(mtime)}")
    else:
        print(f"File {filename:30s} does not exist.")

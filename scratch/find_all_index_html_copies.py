import os
import time

workspace = r"c:\Users\lap4all\Desktop\New folder"
matches = []

for root, dirs, files in os.walk(workspace):
    # skip .git folder to avoid thousands of files, but check refs/logs just in case
    if ".git" in root and "refs" not in root and "logs" not in root:
        continue
    for f in files:
        if "index" in f.lower() and f.endswith(".html"):
            path = os.path.join(root, f)
            mtime = os.path.getmtime(path)
            size = os.path.getsize(path)
            matches.append((path, size, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))))

for m in sorted(matches, key=lambda x: x[0]):
    print(f"Path: {m[0]}\n  Size: {m[1]} bytes | Modified: {m[2]}\n")

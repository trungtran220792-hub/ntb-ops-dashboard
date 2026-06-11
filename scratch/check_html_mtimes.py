import os
import time

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
matches = []

for root, dirs, files in os.walk(workspace_dir):
    for f in files:
        if f.endswith('.html'):
            fullpath = os.path.join(root, f)
            try:
                mtime = os.path.getmtime(fullpath)
                mtime_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
                size = os.path.getsize(fullpath)
                matches.append((fullpath, mtime_str, size))
            except Exception:
                pass

matches.sort(key=lambda x: x[1], reverse=True)

for path, mtime, size in matches:
    print(f"{mtime} | Size: {size} bytes | Path: {path}")

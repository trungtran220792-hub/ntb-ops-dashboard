import os
import time

brain_dir = r"C:\Users\lap4all\.gemini\antigravity-ide\brain"
matches = []

for root, dirs, files in os.walk(brain_dir):
    for f in files:
        if "index" in f.lower() and ("html" in f.lower() or "base" in f.lower() or "patched" in f.lower()):
            path = os.path.join(root, f)
            mtime = os.path.getmtime(path)
            size = os.path.getsize(path)
            matches.append((path, size, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))))

for m in sorted(matches, key=lambda x: x[2]):
    print(f"Path: {m[0]}\n  Size: {m[1]} bytes | Modified: {m[2]}\n")

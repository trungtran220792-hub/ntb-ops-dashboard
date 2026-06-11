import os
import time

brain_dir = r"C:\Users\lap4all\.gemini\antigravity-ide\brain"
dirs = []
for f in os.listdir(brain_dir):
    fpath = os.path.join(brain_dir, f)
    if os.path.isdir(fpath):
        dirs.append((f, os.path.getmtime(fpath)))

dirs.sort(key=lambda x: x[1], reverse=True)
for name, mtime in dirs:
    print(f"{name}: {time.ctime(mtime)}")

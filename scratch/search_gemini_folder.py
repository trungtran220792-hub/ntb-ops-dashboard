# -*- coding: utf-8 -*-
import os
import time

gemini_dir = r"C:\Users\lap4all\.gemini"
matches = []

print(f"Scanning {gemini_dir} recursively...")
for root, dirs, files in os.walk(gemini_dir):
    # skip video recordings to be fast
    if "browser_recordings" in root:
        continue
    for f in files:
        path = os.path.join(root, f)
        try:
            size = os.path.getsize(path)
            if 300000 <= size <= 450000:
                mtime = os.path.getmtime(path)
                mtime_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
                if "2026-06-10" in mtime_str:
                    matches.append((path, size, mtime_str))
        except Exception:
            pass

print(f"\nFound {len(matches)} potential backups under .gemini:")
for m in sorted(matches, key=lambda x: x[2]):
    print(f"Path: {m[0]}\n  Size: {m[1]} bytes | Modified: {m[2]}\n")

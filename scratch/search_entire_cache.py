# -*- coding: utf-8 -*-
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

search_dirs = [
    r"c:\Users\lap4all\Desktop\New folder",
    r"C:\Users\lap4all\.gemini"
]

target_strings = [
    "renderNtbAnalysisTable",
    "tbody-ntb-ltc-analysis",
    "switchNtbRegion",
    "setAmOprSort"
]

matches = []

print("Searching recursively for targets...")
for search_dir in search_dirs:
    if not os.path.exists(search_dir):
        print(f"Directory {search_dir} does not exist.")
        continue
    for root, dirs, files in os.walk(search_dir):
        if "browser_recordings" in root or ".git" in root:
            continue
        for f in files:
            path = os.path.join(root, f)
            # Avoid scanning huge binary files like Excel files
            if f.endswith(('.xlsx', '.png', '.jpg', '.webp', '.zip', '.tar', '.gz', '.mp4')):
                continue
            try:
                size = os.path.getsize(path)
                if size > 20 * 1024 * 1024:  # > 20MB
                    continue
                with open(path, 'rb') as file_obj:
                    # Read sample to avoid blocking on weird devices
                    data = file_obj.read()
                
                found_targets = []
                for t in target_strings:
                    if t.encode('utf-8') in data or t.encode('utf-16') in data:
                        found_targets.append(t)
                
                if found_targets:
                    mtime = os.path.getmtime(path)
                    mtime_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
                    matches.append((path, size, mtime_str, found_targets))
            except Exception as e:
                pass

print(f"\nFound {len(matches)} matching files:")
for m in sorted(matches, key=lambda x: x[2], reverse=True):
    print(f"Path: {m[0]}\n  Size: {m[1]} bytes | Modified: {m[2]}\n  Matched: {m[3]}")

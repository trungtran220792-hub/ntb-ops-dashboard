import os
import time

appdata_roaming = os.environ.get('APPDATA', '')
appdata_local = os.environ.get('LOCALAPPDATA', '')
workspace = r"c:\Users\lap4all\Desktop\New folder"

search_dirs = [
    os.path.join(appdata_roaming, "Code", "User", "History"),
    os.path.join(appdata_local, "Google", "Chrome", "User Data"), # just in case
    workspace
]

matches = []

def scan_dir(directory):
    if not os.path.exists(directory):
        return
    for root, dirs, files in os.walk(directory):
        # skip large irrelevant folders
        if any(x in root for x in ["node_modules", ".git", "Cache", "System Cache", "GPUCache"]):
            continue
        for f in files:
            if "index.html" in f or (len(f) == 40 and not os.path.splitext(f)[1]): # vscode history files have hash names
                path = os.path.join(root, f)
                try:
                    size = os.path.getsize(path)
                    if 300000 <= size <= 450000: # index.html size is around 350KB
                        mtime = os.path.getmtime(path)
                        mtime_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
                        if "2026-06-10" in mtime_str: # only today
                            matches.append((path, size, mtime_str))
                except Exception:
                    pass

for d in search_dirs:
    print(f"Scanning {d}...")
    scan_dir(d)

print(f"\nFound {len(matches)} potential backups:")
for m in sorted(matches, key=lambda x: x[2]):
    print(f"Path: {m[0]}\n  Size: {m[1]} bytes | Modified: {m[2]}\n")

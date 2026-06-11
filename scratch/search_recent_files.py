import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

search_dirs = [
    r"C:\Users\lap4all\Desktop\New folder",
    r"C:\Users\lap4all\.gemini\antigravity-ide",
    r"C:\Users\lap4all\AppData\Local\Temp",
]

target = b"switchNtbRegion"
now = time.time()
one_day = 24 * 3600
count = 0
found = []

print("Scanning for switchNtbRegion in last 24h modified files...")

for s_dir in search_dirs:
    if not os.path.exists(s_dir):
        continue
    for root, dirs, files in os.walk(s_dir):
        # exclude git directories
        if ".git" in root or ".venv" in root or "node_modules" in root:
            continue
        for f in files:
            path = os.path.join(root, f)
            count += 1
            try:
                mtime = os.path.getmtime(path)
                if now - mtime > one_day:
                    continue
                size = os.path.getsize(path)
                if size < 500:
                    continue
                with open(path, "rb") as file_obj:
                    content = file_obj.read()
                if target in content:
                    found.append((path, size, mtime))
                    print(f"Found in: {path} (size: {size} bytes, modified: {time.ctime(mtime)})")
            except Exception:
                pass

print(f"\nScan complete. Scanned {count} files. Found {len(found)} matching files.")

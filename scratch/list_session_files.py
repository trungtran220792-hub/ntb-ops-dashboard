import os
import time

session_dir = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\0d711590-0357-43ee-a937-04cabf62a0ba"
matches = []

for root, dirs, files in os.walk(session_dir):
    for f in files:
        path = os.path.join(root, f)
        mtime = os.path.getmtime(path)
        size = os.path.getsize(path)
        matches.append((path, size, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))))

print(f"Files in {session_dir}:")
for m in sorted(matches, key=lambda x: x[0]):
    # skip .log and video/image files to be concise, but print interesting files
    ext = os.path.splitext(m[0])[1].lower()
    if ext in ['.png', '.webp', '.log']:
        continue
    print(f"  {os.path.relpath(m[0], session_dir)} | Size: {m[1]} | Modified: {m[2]}")

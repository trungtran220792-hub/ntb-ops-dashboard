import os
import time

brain_dir = r"C:\Users\lap4all\.gemini\antigravity-ide\brain"
if os.path.exists(brain_dir):
    dirs = os.listdir(brain_dir)
    print(f"Listing directories under {brain_dir}:")
    for d in dirs:
        path = os.path.join(brain_dir, d)
        if os.path.isdir(path):
            mtime = os.path.getmtime(path)
            mtime_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
            print(f"  {d} | Modified: {mtime_str}")
else:
    print(f"Brain dir not found at {brain_dir}")

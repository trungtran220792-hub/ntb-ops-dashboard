import os
import time
import sys

def check_mtimes():
    sys.stdout.reconfigure(encoding='utf-8')
    files = [
        "app.py",
        "templates/index.html",
        "users.json",
        ".env"
    ]
    
    # Files in scratch
    for f in os.listdir("scratch"):
        fp = os.path.join("scratch", f)
        if os.path.isfile(fp):
            files.append(fp)
            
    # Sort files by modification time
    file_mtimes = []
    for fp in files:
        if os.path.exists(fp):
            mtime = os.path.getmtime(fp)
            file_mtimes.append((fp, mtime))
            
    file_mtimes.sort(key=lambda x: x[1], reverse=True)
    
    print("=== FILES BY MODIFICATION TIME (LATEST FIRST) ===")
    for fp, mtime in file_mtimes[:40]:
        t_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
        size = os.path.getsize(fp)
        print(f"{fp:50} | {t_str} | {size:10,} bytes")

if __name__ == "__main__":
    check_mtimes()

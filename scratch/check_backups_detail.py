import os
import time
import sys

def check_backups():
    sys.stdout.reconfigure(encoding='utf-8')
    candidates = []
    
    # Check current directory and scratch directory
    for root, dirs, files in os.walk("."):
        # Skip .git and __pycache__
        if ".git" in root or "__pycache__" in root:
            continue
        for f in files:
            fp = os.path.join(root, f)
            fl = f.lower()
            if any(x in fl for x in ["base", "patch", "backup", "bak", "orig", "old", "new", "local", "temp", "verify", "diff"]):
                candidates.append(fp)
                
    file_info = []
    for fp in candidates:
        if os.path.exists(fp):
            mtime = os.path.getmtime(fp)
            size = os.path.getsize(fp)
            file_info.append((fp, mtime, size))
            
    file_info.sort(key=lambda x: x[1], reverse=True)
    
    print("=== BACKUP FILES BY MODIFICATION TIME ===")
    for fp, mtime, size in file_info:
        t_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
        print(f"{fp:70} | {t_str} | {size:10,} bytes")

if __name__ == "__main__":
    check_backups()

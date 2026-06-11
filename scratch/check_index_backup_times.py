import os
import time

files = [
    r"c:\Users\lap4all\Desktop\New folder\templates\index.html",
    r"c:\Users\lap4all\Desktop\New folder\scratch\render_index.html",
    r"c:\Users\lap4all\Desktop\New folder\scratch\index.html.base",
    r"c:\Users\lap4all\Desktop\New folder\scratch\index.html.patched",
    r"c:\Users\lap4all\Desktop\New folder\scratch\deployed_index.html",
    r"c:\Users\lap4all\Desktop\New folder\scratch\vercel_index.html"
]

for path in files:
    if os.path.exists(path):
        mtime = os.path.getmtime(path)
        mtime_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
        print(f"{os.path.basename(path)} | Size: {os.path.getsize(path)} | Modified: {mtime_str}")
    else:
        print(f"{os.path.basename(path)} | Does not exist")

import zipfile
import os
import time

zip_path = r"c:\Users\lap4all\Desktop\New folder\dashboard_update.zip"

if os.path.exists(zip_path):
    print(f"File: {zip_path}")
    print(f"Size: {os.path.getsize(zip_path)} bytes")
    mtime = os.path.getmtime(zip_path)
    print(f"Modified: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))}")
    
    with zipfile.ZipFile(zip_path, 'r') as z:
        print("\nFiles inside ZIP:")
        for info in z.infolist()[:50]: # list first 50 files
            print(f"  {info.filename} | Size: {info.file_size} | Date: {info.date_time}")
        if len(z.infolist()) > 50:
            print(f"  ... and {len(z.infolist()) - 50} more files.")
else:
    print("ZIP file not found")

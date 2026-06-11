import zipfile
import os

zip_path = r"c:\Users\lap4all\Desktop\New folder\dashboard_update.zip"

if os.path.exists(zip_path):
    print("Found zip file. Listing contents:")
    with zipfile.ZipFile(zip_path, 'r') as z:
        for info in z.infolist():
            print(f"File: {info.filename}, Size: {info.file_size}")
else:
    print("Zip file not found.")

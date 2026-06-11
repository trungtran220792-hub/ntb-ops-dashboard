import os
import re

base_path = r"c:\Users\lap4all\Desktop\New folder\scratch\index.html.base"
if os.path.exists(base_path):
    print("File size:", os.path.getsize(base_path))
    with open(base_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    print("Total lines:", len(content.splitlines()))
    
    # Search for tabs
    tabs = ["tab-ntb-summary", "tab-volume-creation", "tab-nhan-su", "tab-introduction"]
    for t in tabs:
        match = re.search(rf'id=["\']{t}["\']', content)
        if match:
            print(f"Tab '{t}' found around position {match.start()}")
        else:
            print(f"Tab '{t}' NOT found")
else:
    print("File not found")

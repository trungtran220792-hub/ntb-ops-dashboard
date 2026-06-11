import os
import re

def search_files(directory):
    found = []
    for root, dirs, files in os.walk(directory):
        # Skip .git
        if '.git' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith(('.html', '.js', '.py', '.txt')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if 'handleNtbSort' in content:
                        found.append(filepath)
                except Exception:
                    pass
    return found

found_files = search_files("c:/Users/lap4all/Desktop/New folder")
print("Files containing handleNtbSort:")
for f in found_files:
    print(f)

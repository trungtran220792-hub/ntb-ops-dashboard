import os

search_dirs = [
    r"c:\Users\lap4all\Desktop\New folder",
    r"C:\Users\lap4all\.gemini\antigravity-ide\brain"
]

target_keywords = ["volGrowthWorstChart", "worstOptions", "chart-volume-growth-top"]
found_occurrences = []

for s_dir in search_dirs:
    print(f"Scanning directory: {s_dir}...")
    for root, dirs, files in os.walk(s_dir):
        # Skip .git and pycache
        if ".git" in root or "__pycache__" in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)
            # Skip large media files
            if file.endswith((".webp", ".png", ".xlsx", ".zip", ".csv")):
                continue
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for kw in target_keywords:
                        if kw in content:
                            found_occurrences.append((file_path, kw))
                            print(f"Found keyword '{kw}' in {file_path}")
            except Exception as e:
                pass

print(f"\nSearch complete. Found {len(found_occurrences)} occurrences:")
for path, kw in found_occurrences:
    print(f"- {path} ({kw})")

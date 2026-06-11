import os
import glob

search_paths = [
    r"c:\Users\lap4all\Desktop\New folder",
    r"C:\Users\lap4all\.gemini\antigravity-ide\brain"
]

output = []

def search_keyword_in_files():
    keywords = ["Quản lý Nhân sự", "Gán tất cả", "Gán TTS", "ODR TTS", "Giao lần đầu", "Giao hàng nhanh"]
    # We will walk through all files and search for index.html or files that are large and could be templates.
    for base_dir in search_paths:
        if not os.path.exists(base_dir):
            output.append(f"Directory {base_dir} does not exist.\n")
            continue
        output.append(f"\nScanning {base_dir}...\n")
        for root, dirs, files in os.walk(base_dir):
            # Skip .git and some cache directories
            if ".git" in root or ".venv" in root or "node_modules" in root:
                continue
            for file in files:
                if file.endswith((".html", ".py", ".bak", ".txt", ".json", ".js")):
                    filepath = os.path.join(root, file)
                    # Skip very large files or logs that aren't source files, except JSONL transcripts
                    if os.path.getsize(filepath) > 10000000 and not file.endswith(".jsonl"):
                        continue
                    
                    # Try reading file with different encodings
                    content = None
                    for enc in ["utf-8", "utf-16", "utf-16-le", "latin1"]:
                        try:
                            with open(filepath, "r", encoding=enc) as f:
                                content = f.read()
                                break
                        except:
                            continue
                            
                    if content:
                        found_kws = [kw for kw in keywords if kw.lower() in content.lower()]
                        if found_kws:
                            output.append(f"Found in {filepath} (size {os.path.getsize(filepath)}): {found_kws}\n")

search_keyword_in_files()

with open("scratch/search_all_results.txt", "w", encoding="utf-8") as f:
    f.writelines(output)
print("Done searching.")

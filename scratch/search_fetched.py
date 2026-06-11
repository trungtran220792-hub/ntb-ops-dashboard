import os

file_path = r"scratch/local_html_fetched.html"
output = []

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    output.append(f"Length of local_html_fetched.html: {len(content)}\n")
    
    # Let's search for the sidebar items
    keywords = ["Quản lý Nhân sự", "Gán tất cả", "Gán TTS", "ODR TTS", "Giao lần đầu", "Giao hàng nhanh"]
    for kw in keywords:
        found = kw in content
        output.append(f"Contains '{kw}': {found}\n")
        
    # Find lines containing these keywords
    lines = content.splitlines()
    for idx, line in enumerate(lines, 1):
        for kw in keywords:
            if kw in line:
                output.append(f"Line {idx}: {line.strip()}\n")
else:
    output.append("local_html_fetched.html does not exist.")

with open("scratch/search_fetched_results.txt", "w", encoding="utf-8") as f:
    f.writelines(output)
print("Done searching local_html_fetched.html")

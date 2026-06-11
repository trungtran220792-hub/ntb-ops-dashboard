import os

brain_session_dir = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\2742477c-f9ad-4ec9-923d-4fdf4f5c14ba"
keywords = ["Chỉ số NTB", "Volume tạo đơn", "Quản lý nhân sự"]
results = []

for root, dirs, files in os.walk(brain_session_dir):
    for f in files:
        path = os.path.join(root, f)
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                for kw in keywords:
                    if kw in content:
                        for line_num, line in enumerate(content.splitlines()):
                            if kw in line:
                                results.append(f"File: {os.path.relpath(path, brain_session_dir)} | Line: {line_num+1} | Context: {line.strip()[:150]}")
        except Exception:
            pass

with open("scratch/all_logs_found.txt", "w", encoding="utf-8") as out:
    out.write("\n".join(results))

print(f"Search complete. Found {len(results)} matches. Saved to scratch/all_logs_found.txt")

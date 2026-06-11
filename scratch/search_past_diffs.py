import os

scratch_dir = "scratch"
keywords = ["tab-ntb-summary", "Chỉ số NTB", "tab-volume-creation", "Volume tạo đơn", "tab-nhan-su", "Quản lý nhân sự", "nhan_su"]
results = []

for f in os.listdir(scratch_dir):
    if f.endswith('.txt') or f.endswith('.html') or f.endswith('.js') or f.endswith('.py'):
        path = os.path.join(scratch_dir, f)
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                for kw in keywords:
                    if kw in content:
                        # Find occurrences and print some context
                        for line_num, line in enumerate(content.splitlines()):
                            if kw in line:
                                results.append(f"File: {f} | Line: {line_num+1} | Keyword: {kw} | Context: {line.strip()[:120]}")
        except Exception as e:
            pass

with open("scratch/past_diffs_found.txt", "w", encoding="utf-8") as out:
    out.write("\n".join(results))

print(f"Found {len(results)} occurrences. Saved to scratch/past_diffs_found.txt")

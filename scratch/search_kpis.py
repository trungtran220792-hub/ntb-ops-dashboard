import os

scratch_dir = "scratch"
keywords = ["Gán tất cả", "Gán TTS", "ODR TTS", "Quản lý Nhân sự"]
output = []

for root, dirs, files in os.walk(scratch_dir):
    for file in files:
        filepath = os.path.join(root, file)
        content = None
        for enc in ["utf-8", "utf-16", "utf-16-le", "latin1"]:
            try:
                with open(filepath, "r", encoding=enc) as f:
                    content = f.read()
                    break
            except:
                continue
        if content:
            for kw in keywords:
                if kw.lower() in content.lower():
                    output.append(f"\n=========================================\n")
                    output.append(f"File: {filepath} | Keyword: {kw}\n")
                    # find where it occurs and print 100 characters around it
                    idx = 0
                    while True:
                        idx = content.lower().find(kw.lower(), idx)
                        if idx == -1:
                            break
                        start = max(0, idx - 150)
                        end = min(len(content), idx + 150)
                        output.append(f"Context: ... {repr(content[start:end])} ...\n")
                        idx += len(kw)

with open("scratch/search_kpis_results.txt", "w", encoding="utf-8") as f:
    f.writelines(output)
print("Done searching kpis in scratch.")

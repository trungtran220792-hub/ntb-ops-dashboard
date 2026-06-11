# -*- coding: utf-8 -*-
import os

scratch_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"

def search_in_file(filename, out_f, encoding='utf-8'):
    path = os.path.join(scratch_dir, filename)
    if not os.path.exists(path):
        out_f.write(f"File {filename} does not exist.\n")
        return
    
    out_f.write(f"=== Inspecting {filename} ===\n")
    try:
        if encoding == "utf-16":
            # diff_app_current.txt could be UTF-16, let's try utf-16-le
            with open(path, 'r', encoding='utf-16') as f:
                content = f.read()
        else:
            with open(path, 'r', encoding=encoding) as f:
                content = f.read()
    except Exception as e:
        out_f.write(f"Error reading {filename} with encoding {encoding}: {e}\n")
        return
    
    out_f.write(f"File size: {len(content)} characters\n")
    
    keywords = ["/api/nhan-su", "split_excel_to_csvs", "consolidated_url"]
    for kw in keywords:
        pos = 0
        while True:
            idx = content.find(kw, pos)
            if idx == -1:
                break
            out_f.write(f"Found keyword '{kw}' at index {idx}\n")
            start = max(0, idx - 150)
            end = min(len(content), idx + 1000)
            out_f.write(f"--- Context --- \n{content[start:end]}\n---------------\n")
            pos = idx + len(kw)

with open(os.path.join(scratch_dir, "inspect_diffs_output.txt"), "w", encoding="utf-8") as out_f:
    search_in_file("diff_app_current.txt", out_f, encoding="utf-16")
    search_in_file("diff_app_utf8.txt", out_f, encoding="utf-8")

print("Done writing to inspect_diffs_output.txt")

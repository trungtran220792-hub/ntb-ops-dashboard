# -*- coding: utf-8 -*-
import os

files_to_check = [
    r"c:\Users\lap4all\Desktop\New folder\templates\index.html",
    r"c:\Users\lap4all\Desktop\New folder\scratch\render_index.html",
    r"c:\Users\lap4all\Desktop\New folder\scratch\index.html.base",
    r"c:\Users\lap4all\Desktop\New folder\scratch\index.html.patched"
]

queries = [
    "Báo cáo phân tích & Xếp hạng % LTC",
    "Báo cáo phân tích & Xếp hạng % GTC",
    "setNtbGroupType",
    "renderNtbAnalysisTable",
    "Biểu đồ OPR xếp hạng lỗi trễ của AM",
    "setAmOprSort",
    "renderOprAmChartOnly",
    "Tỷ trọng và lý do trễ hạn OPR",
    "tbody-ntb-ltc-analysis"
]

out = open(r"c:\Users\lap4all\Desktop\New folder\scratch\compare_index_versions_res.txt", "w", encoding="utf-8")

for path in files_to_check:
    if not os.path.exists(path):
        out.write(f"File {path} does not exist\n\n")
        continue
    out.write(f"File: {path}\n")
    out.write(f"  Size: {os.path.getsize(path)} bytes\n")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(path, 'r', encoding='utf-16') as f:
                content = f.read()
        except Exception as e:
            out.write(f"  Error reading file: {str(e)}\n\n")
            continue
    for q in queries:
        count = content.count(q)
        out.write(f"  Query '{q}': {count} occurrences\n")
    out.write("\n")

out.close()
print("Saved comparison results to compare_index_versions_res.txt")

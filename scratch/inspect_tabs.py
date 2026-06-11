# -*- coding: utf-8 -*-
import re
import os

files = [
    r"c:\Users\lap4all\Desktop\New folder\templates\index.html",
    r"c:\Users\lap4all\Desktop\New folder\scratch\index.html.base",
]

out = open(r"c:\Users\lap4all\Desktop\New folder\scratch\inspect_tabs_res.txt", "w", encoding="utf-8")

for p in files:
    if not os.path.exists(p):
        out.write(f"{p} not found\n")
        continue
    out.write(f"\n================ FILE: {os.path.basename(p)} ================\n")
    try:
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(p, 'r', encoding='utf-16') as f:
            content = f.read()

    # Search for sidebar items or tab definitions
    out.write("--- MENU ITEMS (text containing sidebar tags) ---\n")
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if any(keyword in line for keyword in ["Tổng quan", "Nhân sự", "Chỉ số", "Báo cáo", "Backlog", "Bưu cục", "Volume", "Đồng bộ"]):
            if "<li" in line or "<a" in line or "class=" in line or "onclick=" in line or "data-tab" in line or "sidebar" in line:
                out.write(f"Line {i+1}: {line.strip()}\n")

    out.write("--- TAB CONTAINERS (id containing tab-) ---\n")
    for i, line in enumerate(lines):
        if 'id="tab-' in line or 'class="tab-content' in line or 'class="tab-pane' in line:
            out.write(f"Line {i+1}: {line.strip()}\n")

out.close()
print("Done inspecting.")

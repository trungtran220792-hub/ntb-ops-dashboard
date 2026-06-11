# -*- coding: utf-8 -*-
import zipfile
import re
import os

zip_path = r"c:\Users\lap4all\Desktop\New folder\dashboard_update.zip"
out_path = r"c:\Users\lap4all\Desktop\New folder\scratch\inspect_zip_res.txt"

with zipfile.ZipFile(zip_path, 'r') as z:
    content = z.read("templates/index.html").decode("utf-8")

lines = content.split('\n')
out = open(out_path, "w", encoding="utf-8")

out.write("--- ZIP TEMPLATE INSPECTION ---\n")
out.write(f"Total lines: {len(lines)}\n")

out.write("\n--- Sidebar Menu Items ---\n")
in_menu = False
for i, line in enumerate(lines):
    if "sidebar-menu" in line:
        in_menu = True
    if in_menu:
        out.write(f"Line {i+1}: {line.strip()}\n")
        if "</ul>" in line:
            in_menu = False

out.write("\n--- Search for keywords ---\n")
for i, line in enumerate(lines):
    if any(keyword in line for keyword in ["Tổng quan", "Nhân sự", "Chỉ số", "Báo cáo", "Backlog", "Bưu cục", "Volume", "Đồng bộ"]):
        if "<li" in line or "<a" in line or "class=" in line or "onclick=" in line or "data-tab" in line:
            out.write(f"Line {i+1}: {line.strip()}\n")

out.write("\n--- Tab ids ---\n")
for i, line in enumerate(lines):
    if 'id="tab-' in line:
        out.write(f"Line {i+1}: {line.strip()}\n")

out.close()
print("Saved zip inspection to inspect_zip_res.txt")

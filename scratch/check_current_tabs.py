# -*- coding: utf-8 -*-
import sys

filepath = r"c:\Users\lap4all\Desktop\New folder\templates\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

out = open(r"c:\Users\lap4all\Desktop\New folder\scratch\current_tabs_info.txt", "w", encoding="utf-8")

def print_section(section_id):
    start = -1
    end = -1
    depth = 0
    for i, line in enumerate(lines):
        if f'id="{section_id}"' in line:
            start = i
            depth = 1
            out.write(f"Found {section_id} starting at line {i+1}: {line.strip()}\n")
            continue
        if start != -1:
            open_divs = line.count("<div")
            close_divs = line.count("</div>")
            depth += open_divs - close_divs
            if depth <= 0:
                end = i
                out.write(f"Found {section_id} ending at line {i+1}: {line.strip()}\n")
                break
    
    if start != -1 and end != -1:
        out.write(f"--- CONTENT OF {section_id} ({end - start + 1} lines) ---\n")
        for line_idx in range(start, min(start + 50, end + 1)):
            out.write(f"{line_idx+1}: {lines[line_idx].rstrip()}\n")
        if end - start > 50:
            out.write("...\n")
            for line_idx in range(max(start + 50, end - 20), end + 1):
                out.write(f"{line_idx+1}: {lines[line_idx].rstrip()}\n")

print_section("tab-ntb-summary")
print_section("tab-opr")

out.close()
print("Saved info to current_tabs_info.txt")

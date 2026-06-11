# -*- coding: utf-8 -*-
import os

steps_dir = r"c:\Users\lap4all\Desktop\New folder\scratch\extracted_steps"
files = sorted(os.listdir(steps_dir))

out = open(r"c:\Users\lap4all\Desktop\New folder\scratch\steps_detail_summary.txt", "w", encoding="utf-8")

for filename in files:
    filepath = os.path.join(steps_dir, filename)
    out.write(f"\n=========================================\n")
    out.write(f"FILE: {filename}\n")
    out.write(f"=========================================\n")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Let's extract TargetContent/ReplacementContent or print the whole file if it is small,
    # or print the first 50 lines and last 50 lines.
    lines = content.splitlines()
    if len(lines) <= 120:
        out.write(content)
    else:
        out.write(f"Total lines: {len(lines)}\n")
        out.write("--- FIRST 60 LINES ---\n")
        out.write("\n".join(lines[:60]))
        out.write("\n...\n")
        out.write("--- LAST 60 LINES ---\n")
        out.write("\n".join(lines[-60:]))
    out.write("\n")

out.close()
print("Saved summary to steps_detail_summary.txt")

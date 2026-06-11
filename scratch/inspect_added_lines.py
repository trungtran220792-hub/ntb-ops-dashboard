# -*- coding: utf-8 -*-
import os

scratch_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"

def inspect_added_lines():
    diff_path = os.path.join(scratch_dir, "temp_index_diff.txt")
    out_path = os.path.join(scratch_dir, "added_lines.txt")
    if not os.path.exists(diff_path):
        print("temp_index_diff.txt does not exist")
        return
        
    with open(diff_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        
    with open(out_path, "w", encoding="utf-8") as out:
        for line in lines:
            if line.startswith("@@") or line.startswith("+++") or line.startswith("---") or line.startswith("+"):
                # Avoid printing lines that are just single '+' or empty
                if line.startswith("+") and not line.startswith("+++") and len(line.strip()) <= 1:
                    continue
                out.write(line)
                
    print("Done writing to added_lines.txt")

inspect_added_lines()

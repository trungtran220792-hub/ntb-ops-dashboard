# -*- coding: utf-8 -*-
import os

scratch_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"

def analyze_git_diff_index():
    path = os.path.join(scratch_dir, "git_diff_index.txt")
    if not os.path.exists(path):
        print("git_diff_index.txt does not exist")
        return
        
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        
    print(f"Total lines: {len(lines)}")
    
    # Print lines that look like additions of tabs or sections
    for i, line in enumerate(lines):
        if line.startswith("+++") or line.startswith("---") or line.startswith("@@"):
            print(f"Line {i}: {line.strip()}")
            
analyze_git_diff_index()

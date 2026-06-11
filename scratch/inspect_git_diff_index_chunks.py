# -*- coding: utf-8 -*-
import os

scratch_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"

def analyze_git_diff_index_chunks():
    path = os.path.join(scratch_dir, "git_diff_index.txt")
    out_path = os.path.join(scratch_dir, "inspect_git_diff_index_chunks_output.txt")
    if not os.path.exists(path):
        print("git_diff_index.txt does not exist")
        return
        
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        
    with open(out_path, "w", encoding="utf-8") as out:
        current_chunk = []
        in_chunk = False
        for line in lines:
            if line.startswith("@@"):
                if current_chunk:
                    out.write("".join(current_chunk))
                    out.write("\n" + "="*80 + "\n\n")
                current_chunk = [line]
                in_chunk = True
            elif in_chunk:
                # Add line to current chunk if it shows modification (+ or -) or is context
                current_chunk.append(line)
        if current_chunk:
            out.write("".join(current_chunk))
            
    print("Done writing to inspect_git_diff_index_chunks_output.txt")

analyze_git_diff_index_chunks()

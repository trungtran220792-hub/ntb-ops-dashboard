import os
import sys

def check_intro():
    sys.stdout.reconfigure(encoding='utf-8')
    files = ["templates/index.html", "scratch/index.html.base", "scratch/index_base_utf8.html", "scratch/render_index.html"]
    for f in files:
        if os.path.exists(f):
            print(f"=== File: {f} ===")
            with open(f, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()
            # Find occurrences of switchTab('tab-introduction'
            for idx, line in enumerate(lines):
                if "tab-introduction" in line and "onclick" in line:
                    print(f"  Line {idx+1}: {line.strip()[:120]}")

if __name__ == "__main__":
    check_intro()

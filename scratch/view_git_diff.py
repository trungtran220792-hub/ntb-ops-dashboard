# -*- coding: utf-8 -*-
import subprocess
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"

res = subprocess.run(["git", "diff", "templates/index.html"], cwd=workspace_dir, capture_output=True, text=True, encoding="utf-8", errors="ignore")
print("DIFF STDOUT LENGTH:", len(res.stdout))

with open(os.path.join(workspace_dir, "scratch", "git_diff_index.txt"), "w", encoding="utf-8") as out:
    out.write(res.stdout)

print("Saved diff to scratch/git_diff_index.txt")

import subprocess
import os

res = subprocess.run(["git", "diff", "templates/index.html"], capture_output=True)
with open("scratch/git_diff_index_utf8.txt", "wb") as f:
    f.write(res.stdout)

print("Saved git diff to scratch/git_diff_index_utf8.txt. Size:", len(res.stdout))

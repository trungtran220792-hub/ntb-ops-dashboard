# -*- coding: utf-8 -*-
import subprocess
import os

scratch_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"

# Let's run a git diff between HEAD and the backup file to see exactly what changes are there
# First, let's copy templates_index_backup_before_reset.html to a temp file in the workspace
# and diff it with git HEAD.
temp_diff_path = os.path.join(scratch_dir, "temp_index_diff.txt")
try:
    # Run git diff between HEAD and the backup file
    # We can do this by running a git diff command with --no-index or just diffing them
    cmd = ["git", "diff", "--no-index", "templates/index.html", r"scratch/templates_index_backup_before_reset.html"]
    # Since templates/index.html is reset to git HEAD, this will show exactly what was added in the backup!
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    with open(temp_diff_path, "w", encoding="utf-8") as f:
        f.write(res.stdout)
    print(f"Diff output size: {len(res.stdout)} bytes")
    
    # Print the line changes that were added (lines starting with @@ or + or -)
    diff_lines = res.stdout.splitlines()
    for idx, line in enumerate(diff_lines[:100]):
        print(line)
        
except Exception as e:
    print(f"Error running git diff: {e}")

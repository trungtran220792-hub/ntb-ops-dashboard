# -*- coding: utf-8 -*-
import subprocess
import os

scratch_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"
cmd = ["git", "diff", "--no-index", "app.py", r"scratch/app_backup_before_reset.py"]
res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')

with open(os.path.join(scratch_dir, "compare_app_versions_output.txt"), "w", encoding="utf-8") as f:
    f.write(res.stdout)

print(f"Diff size: {len(res.stdout)} bytes")
# Print first 50 lines of diff
lines = res.stdout.splitlines()
for l in lines[:50]:
    print(l)

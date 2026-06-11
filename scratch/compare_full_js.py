with open("c:/Users/lap4all/Desktop/New folder/templates/index.html", 'r', encoding='utf-8') as f:
    curr_html = f.read()

with open("c:/Users/lap4all/Desktop/New folder/scratch/templates_index_backup_before_reset.html", 'r', encoding='utf-8') as f:
    back_html = f.read()

# Extract all script blocks
import re
curr_scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', curr_html, re.DOTALL)
back_scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', back_html, re.DOTALL)

print(f"Current script blocks: {len(curr_scripts)}")
print(f"Backup script blocks: {len(back_scripts)}")

# If there's a main long script block, let's compare that.
# Let's find the largest script block in each.
curr_main = max(curr_scripts, key=len) if curr_scripts else ""
back_main = max(back_scripts, key=len) if back_scripts else ""

print(f"Main script lengths - Current: {len(curr_main)}, Backup: {len(back_main)}")
if curr_main == back_main:
    print("Main script block is IDENTICAL!")
else:
    print("Main script block is DIFFERENT!")
    # Let's save both to separate files in scratch so we can diff them or run a diff on them
    with open("c:/Users/lap4all/Desktop/New folder/scratch/main_script_curr.js", "w", encoding="utf-8") as f:
        f.write(curr_main)
    with open("c:/Users/lap4all/Desktop/New folder/scratch/main_script_back.js", "w", encoding="utf-8") as f:
        f.write(back_main)
    print("Saved script blocks to scratch/main_script_curr.js and scratch/main_script_back.js")

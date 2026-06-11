import difflib

with open("c:/Users/lap4all/Desktop/New folder/templates/index.html", "r", encoding="utf-8") as f:
    curr = f.readlines()

with open("c:/Users/lap4all/Desktop/New folder/scratch/templates_index_backup_before_reset.html", "r", encoding="utf-8") as f:
    back = f.readlines()

diff = list(difflib.unified_diff(
    curr,
    back,
    fromfile="Current HTML",
    tofile="Backup HTML",
    n=3
))

print(f"Diff lines count: {len(diff)}")
with open("c:/Users/lap4all/Desktop/New folder/scratch/full_html_diff.txt", "w", encoding="utf-8") as f:
    f.writelines(diff)
print("Saved full diff to scratch/full_html_diff.txt")

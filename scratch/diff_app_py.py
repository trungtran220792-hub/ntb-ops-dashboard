import difflib

with open("c:/Users/lap4all/Desktop/New folder/app.py", "r", encoding="utf-8") as f:
    curr = f.readlines()

with open("c:/Users/lap4all/Desktop/New folder/scratch/app_backup_before_reset.py", "r", encoding="utf-8") as f:
    back = f.readlines()

diff = list(difflib.unified_diff(
    curr,
    back,
    fromfile="Current app.py",
    tofile="Backup app.py",
    n=3
))

print(f"Diff lines count: {len(diff)}")
with open("c:/Users/lap4all/Desktop/New folder/scratch/app_py_diff.txt", "w", encoding="utf-8") as f:
    f.writelines(diff)
print("Saved full app.py diff to scratch/app_py_diff.txt")

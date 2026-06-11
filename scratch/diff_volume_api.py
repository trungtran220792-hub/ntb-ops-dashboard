import difflib

with open("c:/Users/lap4all/Desktop/New folder/scratch/volume_api_curr.py", "r", encoding="utf-8") as f:
    curr = f.readlines()

with open("c:/Users/lap4all/Desktop/New folder/scratch/volume_api_back.py", "r", encoding="utf-8") as f:
    back = f.readlines()

diff = list(difflib.unified_diff(
    curr,
    back,
    fromfile="Current API",
    tofile="Backup API",
    n=3
))

with open("c:/Users/lap4all/Desktop/New folder/scratch/volume_api_diff.txt", "w", encoding="utf-8") as f:
    f.writelines(diff)

print("Saved diff to scratch/volume_api_diff.txt")

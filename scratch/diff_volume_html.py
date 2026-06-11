from compare_tab_contents import extract_div
import difflib

v_curr = extract_div("c:/Users/lap4all/Desktop/New folder/templates/index.html", "tab-volume-creation")
v_back = extract_div("c:/Users/lap4all/Desktop/New folder/scratch/templates_index_backup_before_reset.html", "tab-volume-creation")

diff = list(difflib.unified_diff(
    v_curr.splitlines(keepends=True),
    v_back.splitlines(keepends=True),
    fromfile="Current Volume HTML",
    tofile="Backup Volume HTML",
    n=3
))

print(f"Diff lines: {len(diff)}")
with open("c:/Users/lap4all/Desktop/New folder/scratch/volume_html_diff.txt", "w", encoding="utf-8") as f:
    f.writelines(diff)
print("Saved diff to scratch/volume_html_diff.txt")

import re

diff_path = "scratch/git_diff_index_full.txt"
added_blocks = []
removed_blocks = []

current_added = []
current_removed = []

with open(diff_path, 'r', encoding='utf-16') as f:
    for line in f:
        if line.startswith('@@'):
            if current_added:
                added_blocks.append("".join(current_added))
                current_added = []
            if current_removed:
                removed_blocks.append("".join(current_removed))
                current_removed = []
            added_blocks.append(f"Hunk: {line.strip()}")
        elif line.startswith('+') and not line.startswith('+++'):
            current_added.append(line[1:])
        elif line.startswith('-') and not line.startswith('---'):
            current_removed.append(line[1:])
        else:
            if current_added:
                added_blocks.append("".join(current_added))
                current_added = []
            if current_removed:
                removed_blocks.append("".join(current_removed))
                current_removed = []

if current_added:
    added_blocks.append("".join(current_added))
if current_removed:
    removed_blocks.append("".join(current_removed))

# Print summary of hunks and changes
print("Number of added code blocks:", len(added_blocks))
print("Number of removed code blocks:", len(removed_blocks))

# Let's write the analyzed hunks to a text file for review
with open("scratch/diff_summary_detailed.txt", "w", encoding="utf-8") as out:
    for item in added_blocks:
        if item.startswith("Hunk:"):
            out.write(f"\n{item}\n" + "-"*40 + "\n")
        else:
            out.write(f"ADDED:\n{item}\n")

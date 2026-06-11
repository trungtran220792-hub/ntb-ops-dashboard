with open("c:/Users/lap4all/Desktop/New folder/scratch/full_html_diff.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Let's find Section 14 (the 14th occurrence of "@@")
sec_count = 0
sec_lines = []
for l in lines:
    if l.startswith("@@"):
        sec_count += 1
    if sec_count == 14:
        sec_lines.append(l)
    elif sec_count > 14:
        break

print(f"=== Section 14 Diff lines (count: {len(sec_lines)}) ===")
# Write to a file in UTF-8
with open("c:/Users/lap4all/Desktop/New folder/scratch/section_14_diff.txt", "w", encoding="utf-8") as f:
    f.writelines(sec_lines)
print("Saved Section 14 diff to scratch/section_14_diff.txt")

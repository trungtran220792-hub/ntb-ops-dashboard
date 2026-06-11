with open("c:/Users/lap4all/Desktop/New folder/templates/index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

found = []
for i, line in enumerate(lines):
    if "đạt" in line.lower():
        found.append(f"{i+1}: {line.strip()}")

with open("c:/Users/lap4all/Desktop/New folder/scratch/search_dat_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(found))

print(f"Found {len(found)} matching lines. Saved to scratch/search_dat_res.txt")

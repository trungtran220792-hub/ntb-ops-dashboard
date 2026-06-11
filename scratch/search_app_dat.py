with open("c:/Users/lap4all/Desktop/New folder/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

found = []
for i, line in enumerate(lines):
    if "đạt" in line.lower() or "chuadat" in line.lower() or "chưa đạt" in line.lower():
        found.append(f"L{i+1}: {line.strip()}")

with open("c:/Users/lap4all/Desktop/New folder/scratch/search_app_dat_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(found))

print(f"Found {len(found)} matching lines in app.py. Saved to scratch/search_app_dat_res.txt")

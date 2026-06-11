with open("c:/Users/lap4all/Desktop/New folder/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

out = []
for i, line in enumerate(lines):
    if "/api/nhan-su" in line:
        start = max(0, i - 5)
        end = min(len(lines), i + 10)
        out.append("".join(lines[start:end]))
        break

with open("c:/Users/lap4all/Desktop/New folder/scratch/nhan_su_api_decor.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("Saved nhan su decorator to scratch/nhan_su_api_decor.txt")

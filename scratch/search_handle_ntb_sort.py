with open("c:/Users/lap4all/Desktop/New folder/templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer("handleNtbSort", content)]

out = []
out.append(f"Matches found at positions: {matches}")

for idx in matches:
    start = max(0, idx - 100)
    end = min(len(content), idx + 800)
    out.append(f"\n--- Position {idx} ---")
    out.append(content[start:end])
    out.append("-" * 50)

with open("c:/Users/lap4all/Desktop/New folder/scratch/ntb_sort_context.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("Saved NTB sort context to scratch/ntb_sort_context.txt")

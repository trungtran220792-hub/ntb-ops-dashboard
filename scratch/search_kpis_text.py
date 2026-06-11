with open("c:/Users/lap4all/Desktop/New folder/templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
keywords = ["chưa đạt", "đạt", "chua dat", "dat", "kpi-", "badge-", "card-"]
out = []
for kw in keywords:
    matches = [m.start() for m in re.finditer(kw, content, re.IGNORECASE)]
    out.append(f"Keyword '{kw}' matches: {len(matches)}")
    # If there are fewer than 10 matches, print contexts
    if len(matches) < 20:
        for idx in matches:
            context = content[max(0, idx - 80):min(len(content), idx + 80)]
            out.append(f"  idx {idx}: {context.strip()}")

with open("c:/Users/lap4all/Desktop/New folder/scratch/search_kpis_text_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("Saved search results to scratch/search_kpis_text_res.txt")

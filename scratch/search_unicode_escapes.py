with open("c:/Users/lap4all/Desktop/New folder/templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
# Unicode escapes: \u0111 (đ), \u1ea1 (ạt), \u0110 (Đ)
escapes = [r'\\u0111\\u1ea1t', r'\\u0110\\u1ea1t', r'Ch\u01b0a', r'\\u01b0a']
out = []
for esc in escapes:
    matches = [m.start() for m in re.finditer(esc, content, re.IGNORECASE)]
    out.append(f"Escape '{esc}' matches: {len(matches)}")
    for idx in matches[:10]:
        context = content[max(0, idx - 80):min(len(content), idx + 80)]
        out.append(f"  idx {idx}: {context.strip()}")

with open("c:/Users/lap4all/Desktop/New folder/scratch/search_unicode_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("Saved unicode search results to scratch/search_unicode_res.txt")

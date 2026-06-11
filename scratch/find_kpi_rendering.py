with open("c:/Users/lap4all/Desktop/New folder/templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
elements = ["kpi-ltc-value", "kpi-gtc-value", "kpi-ttc-value", "kpi-ltc-badge", "kpi-gtc-badge", "kpi-ttc-badge"]
out = []
for el in elements:
    matches = [m.start() for m in re.finditer(el, content)]
    out.append(f"Element '{el}' matches: {len(matches)}")
    for idx in matches:
        start = max(0, idx - 150)
        end = min(len(content), idx + 800)
        out.append(f"\n--- Context for '{el}' at position {idx} ---")
        out.append(content[start:end])
        out.append("-" * 50)

with open("c:/Users/lap4all/Desktop/New folder/scratch/kpi_rendering_context.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("Saved rendering contexts to scratch/kpi_rendering_context.txt")

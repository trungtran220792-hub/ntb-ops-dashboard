with open("c:/Users/lap4all/Desktop/New folder/templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
out = []

matches = re.findall(r'<[^>]+(?:onclick|id|class)=[^>]*telegram[^>]*>', content, re.IGNORECASE)
out.append(f"Telegram tags found: {len(matches)}")
for m in matches:
    out.append("  " + m.strip())

matches_text = re.findall(r'[^<>]*telegram[^<>]*', content, re.IGNORECASE)
out.append(f"Text nodes with Telegram: {len(matches_text)}")
for mt in matches_text:
    if mt.strip():
        out.append("  " + mt.strip())

with open("c:/Users/lap4all/Desktop/New folder/scratch/telegram_html_results.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("Saved results to scratch/telegram_html_results.txt")

# -*- coding: utf-8 -*-
import os, glob

# Let's search all files in scratch/ for any Google Sheets URL that starts with docs.google.com
# and doesn't match the 7 separate ones in config.json.
seen_urls = [
    "1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk",
    "1B-QCbEnPpILFFEWPYheGdmkgYV9gSf4lAyQMlhzwOCM",
    "1WCzgao34cA_SttyB9ytHfE1qKTNl_3iFqDbEfw3lbyU",
    "1MjLW8NbD5ZjoOdd90myGv0i1NGAtlvScxebfAXMM1j8",
    "1lmQv8KwHJzDFs_RMz64ydu4SOmG3M1YAzILNFGtzFec",
    "1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg",
    "1OygEPTn6Qu8okwAqpbx_RBiYQr1cfpO5hiaxqu4AMNE"
]

with open(r"scratch\found_urls.txt", "w", encoding="utf-8") as out:
    for f in glob.glob(r"scratch\*") + glob.glob(r"*"):
        if os.path.isfile(f) and f.endswith((".txt", ".py", ".json", ".html", ".env")):
            try:
                content = open(f, "r", encoding="utf-8", errors="ignore").read()
                # Find all spreadsheet URLs
                import re
                urls = re.findall(r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)', content)
                for u in urls:
                    if u not in seen_urls:
                        out.write(f"File {f}: found non-default sheet ID: {u}\n")
                        # Also print the full URL context
                        pos = content.find(u)
                        out.write(f"  Context: {content[max(0, pos-100):min(len(content), pos+150)]}\n")
            except:
                pass
print("Done")

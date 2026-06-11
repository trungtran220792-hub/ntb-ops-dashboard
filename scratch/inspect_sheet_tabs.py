import urllib.request
import re

url = "https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit"
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')

out_lines = []
def my_print(*args):
    out_lines.append(" ".join(map(str, args)))

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    
    # Find all divs containing 'docs-sheet-tab'
    # E.g., <div class="docs-sheet-tab goog-inline-block" id="sheet-button-1365110988">...Caption...</div>
    # Let's search using regex
    # We want to find the ID and the text content inside the class="goog-inline-block docs-sheet-tab-caption"
    
    # Let's search for matches of sheet tabs:
    # Google sheet tabs are like:
    # id="sheet-button-1365110988" or similar
    # Let's inspect text around id="sheet-button-
    matches = re.findall(r'id=["\']sheet-button-([^"\']+)["\']', html)
    my_print("Sheet button IDs found:", len(matches))
    for m in matches:
        my_print("Button ID:", m)
        
    # Let's try to grab the whole block of the bottom bar
    pos = html.find('id="grid-bottom-bar"')
    if pos != -1:
        my_print("Found grid-bottom-bar!")
        snippet = html[pos:pos+40000]
        # Find all tab structures:
        # id="sheet-button-GID" ... class="goog-inline-block docs-sheet-tab-caption">TITLE</div>
        tab_matches = re.findall(r'id=["\']sheet-button-([^"\']+)["\'].*?class=["\'][^"\']*docs-sheet-tab-caption[^"\']*["\']>(.*?)</div>', snippet)
        my_print("Tab matches in bottom bar snippet:", len(tab_matches))
        for gid, title in tab_matches:
            my_print(f"  {title.strip()} -> {gid}")
            
except Exception as e:
    my_print("Error:", e)

with open("scratch/inspect_sheet_tabs_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))
print("Done writing scratch/inspect_sheet_tabs_res.txt")

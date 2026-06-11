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
    
    # Let's search for some candidates in the HTML
    candidates = ["Data", "DataLTC", "rawltc", "Cơ cấu", "tts", "opr", "raw n-1", "rawopr", "aging", "treo lc", "ntb", "đang off", "shopee_tiktok", "odr tts", "nhân sự"]
    
    my_print("Search results:")
    for cand in candidates:
        pos = html.lower().find(cand.lower())
        if pos != -1:
            snippet = html[max(0, pos-100):min(len(html), pos+200)]
            # remove newlines/tabs for clean print
            snippet = " ".join(snippet.split())
            my_print(f"Candidate '{cand}' found at index {pos}. Surrounding: {snippet}")
        else:
            my_print(f"Candidate '{cand}' NOT found.")
            
    # Search for all strings matching a number followed by sheet metadata
    # e.g., list of sheets
    # Google Sheet often puts sheets in a script tag as:
    # {"id":0,"title":"Data"} or similar
    # Let's find any JSON patterns like "id":\d+,"title":
    json_matches = re.findall(r'(\d+)\s*,\s*0\s*,\s*"(\d+)"\s*,\s*\[\s*\{\s*"1"\s*:\s*\[\s*\[\s*0\s*,\s*0\s*,\s*"([^"]+)"', html)
    my_print("Regex 1 matches:", len(json_matches))
    for m in json_matches:
        my_print(m)
        
    # Let's search for "gid" or "sheetId" or "gridId"
    for term in ["gid", "sheetid", "gridid", "sheetId"]:
        c = len(re.findall(re.escape(term), html, re.IGNORECASE))
        my_print(f"Occurrences of '{term}': {c}")
        
except Exception as e:
    my_print("Error:", e)

with open("scratch/find_sheet_gids_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))
print("Done writing scratch/find_sheet_gids_res.txt")

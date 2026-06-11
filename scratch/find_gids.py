import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/edit"
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')

print("Fetching sheet list...")
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    
    # Google sheets JSON model contains sheet properties like:
    # {"properties":{"sheetId":1884142015,"title":"ODR TTS","index":9,"sheetType":"GRID",...}}
    matches = re.findall(r'"sheetId"\s*:\s*(\d+)\s*,\s*"title"\s*:\s*"([^"]+)"', html)
    print(f"Found {len(matches)} sheets via pattern 1:")
    for gid, title in matches:
        print(f"  - '{title}': {gid}")
        
    matches2 = re.findall(r'"title"\s*:\s*"([^"]+)"\s*,\s*"sheetId"\s*:\s*(\d+)', html)
    print(f"Found {len(matches2)} sheets via pattern 2:")
    for title, gid in matches2:
        print(f"  - '{title}': {gid}")
        
    # Let's search for sheetId in any context
    # format like: "sheetId":1884142015
    gids_only = re.findall(r'"sheetId"\s*:\s*(\d+)', html)
    titles_only = re.findall(r'"title"\s*:\s*"([^"]+)"', html)
    print(f"GIDs count: {len(gids_only)}, Titles count: {len(titles_only)}")
except Exception as e:
    print("Error:", e)

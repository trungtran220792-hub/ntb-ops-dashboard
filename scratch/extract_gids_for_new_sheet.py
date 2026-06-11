import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit"
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

try:
    with urllib.request.urlopen(req) as res:
        print(f"Status: {res.status}")
        html = res.read().decode('utf-8')
    
    print(f"HTML length: {len(html)}")
    with open("scratch/sheet_html.txt", "w", encoding="utf-8") as f:
        f.write(html[:100000]) # write first 100k characters to inspect
        
    results = {}
    
    # Try finding any sheetId or name pattern
    # Google sheets JSON format:
    # "bootstrapData" usually contains a JSON representation of sheets
    # let's look for sheetId:
    for match in re.finditer(r'"sheetId"\s*:\s*(\d+)', html):
        print(f"Found sheetId match: {match.group(0)}")
        
    for match in re.finditer(r'"name"\s*:\s*"([^"]+)"', html):
        # limit printing
        pass

    # Simple regexes to find names and sheetIds
    matches = re.findall(r'"name"\s*:\s*"([^"]+)"\s*,\s*"sheetId"\s*:\s*(\d+)', html)
    for name, gid in matches:
        results[name] = gid
        
    matches2 = re.findall(r'"sheetId"\s*:\s*(\d+)\s*,\s*"name"\s*:\s*"([^"]+)"', html)
    for gid, name in matches2:
        results[name] = gid

    matches3 = re.findall(r'\\"(?P<gid>\d+)\\",(?:\s*0\s*,)?\s*\\"(?P<name>[^\\"]+)\\"', html)
    for gid, name in matches3:
        if len(gid) > 3:
            results[name] = gid

    print(f"Found {len(results)} results:")
    for name, gid in sorted(results.items()):
        print(f"Tab: {name} -> GID: {gid}")
        
except Exception as e:
    print(f"Error: {e}")

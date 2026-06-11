import json
import re
import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

def get_gids_robust(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            html = response.read().decode('utf-8')
        
        results = []
        # Match escaped json like: 198\",[{\\\"1\\\":[[0,0,\\\"Thứ cùng kỳ\\\"
        # Which is: (\d+)\\",\[\{\\\"1\\\":\[\[0,0,\\\"([^\"]+)\\\"
        matches = re.finditer(r'(\d+)\\",\[\{\\"1\\":\[\[0,0,\\"([^\\"]+)\\"', html)
        for m in matches:
            results.append((m.group(2), m.group(1)))
            
        # Try raw json like: {"name":"<name>","sheetId":<id>}
        matches_v2 = re.findall(r'"name"\s*:\s*"([^"]+)"\s*,\s*"sheetId"\s*:\s*(\d+)', html)
        for name, gid in matches_v2:
            if (name, gid) not in results:
                results.append((name, gid))
                
        matches_v3 = re.findall(r'"sheetId"\s*:\s*(\d+)\s*,\s*"name"\s*:\s*"([^"]+)"', html)
        for gid, name in matches_v3:
            if (name, gid) not in results:
                results.append((name, gid))

        # Check for sheet metadata inside JS arrays e.g. [gid, name] or similar
        # e.g., ["1365110988","DataLTC"] or similar
        matches_v4 = re.finditer(r'\\"(?P<gid>\d+)\\",(?:\s*0\s*,)?\s*\\"(?P<name>[^\\"]+)\\"', html)
        for m in matches_v4:
            name = m.group('name')
            gid = m.group('gid')
            if len(gid) > 3 and (name, gid) not in results:
                results.append((name, gid))
                
        return results
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return []

def main():
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        
    for key in ["ops_url", "opr_url", "aging_url", "treo_url", "bat_on_url", "off_spe_url", "tao_don_url"]:
        url = config.get(key)
        print(f"\nSpreadsheet for {key}:")
        if not url:
            print("  Empty URL")
            continue
        # Strip gid if present to get main URL
        base_url = url
        match = re.search(r'(/spreadsheets/d/[a-zA-Z0-9-_]+)', url)
        if match:
            base_url = "https://docs.google.com/spreadsheets/d/" + match.group(1).split('/')[-1] + "/edit"
        print(f"  Base URL: {base_url}")
        tabs = get_gids_robust(base_url)
        if not tabs:
            print("  No tabs found via robust search")
        for name, gid in tabs:
            print(f"  Tab: '{name}' -> GID: '{gid}'")

if __name__ == '__main__':
    main()

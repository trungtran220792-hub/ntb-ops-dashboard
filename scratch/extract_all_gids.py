import json
import re
import urllib.request

def get_gids(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
        
        # Look for sheet info patterns in bootstrapData
        # e.g., [gid, name, index] or similar JSON-like structures
        # We can find all occurrences of "gid" or look for matches like: [1884142015,"Sheet Name",...]
        # A common pattern is: [id, 0, "gid", [{"1":[[0,0,"name"]]
        # Let's extract any occurrence of a number followed by the sheet name in double quotes
        # Or look for '"gid":"<number>"' or similar
        # Let's print out some parts or use regex to search for tab names:
        results = []
        matches = re.finditer(r'\[\d+,\s*0,\s*"([^"]+)",\s*\[\s*\{\s*"1"\s*:\s*\[\s*\[\s*0,\s*0,\s*"([^"]+)"', html)
        for m in matches:
            results.append((m.group(2), m.group(1)))
            
        matches_v2 = re.findall(r'"([^"]+)"\s*,\s*\[\s*\{\s*"1"\s*:\s*\[\s*\[\s*0,\s*0,\s*"([^"]+)"', html)
        for gid, name in matches_v2:
            if (name, gid) not in results:
                results.append((name, gid))

        # Additional regex fallback
        matches_v3 = re.findall(r'\[(\d+),\d+,"([^"]+)",', html)
        for gid, name in matches_v3:
            if len(gid) > 3 and (name, gid) not in results:
                results.append((name, gid))

        # Check for sheet metadata inside scripts: {"name":"<name>","sheetId":<id>}
        matches_v4 = re.findall(r'"name"\s*:\s*"([^"]+)"\s*,\s*"sheetId"\s*:\s*(\d+)', html)
        for name, gid in matches_v4:
            if (name, gid) not in results:
                results.append((name, gid))
                
        matches_v5 = re.findall(r'"sheetId"\s*:\s*(\d+)\s*,\s*"name"\s*:\s*"([^"]+)"', html)
        for gid, name in matches_v5:
            if (name, gid) not in results:
                results.append((name, gid))
                
        return results
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return []

def main():
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        
    for key, url in config.items():
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
        tabs = get_gids(base_url)
        for name, gid in tabs:
            print(f"  Tab: '{name}' -> GID: '{gid}'")

if __name__ == '__main__':
    main()

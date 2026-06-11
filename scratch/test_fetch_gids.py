import urllib.request
import re
import sys

url = "https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit"
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')

out_lines = []
def my_print(*args):
    out_lines.append(" ".join(map(str, args)))

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    
    my_print("HTML length:", len(html))
    
    # Let's search for sheet IDs and names.
    # Pattern 1: [sheet_index, 0, "gid", [{"1":[[0,0,"Title"]]
    matches = re.findall(r'\[\d+,\s*0,\s*"(\d+)",\s*\[\s*\{\s*"1"\s*:\s*\[\s*\[\s*\d+,\s*\d+,\s*"([^"]+)"', html)
    my_print("Matches found:", len(matches))
    for gid, title in matches:
        my_print(f"  {title} -> {gid}")
        
    # Let's try matching a simpler pattern:
    # Google Sheet JSON data: "sheetId": 12345, "title": "SheetName" or similar.
    # Let's check for title and sheetId in the initial data block
    if not matches:
        # Check initial data block
        match_initial = re.findall(r'\\"[tT]itle\\"\s*:\s*\\"[^\\"]+\\",\s*\\"[sS]heetId\\"\s*:\s*(\d+)', html)
        my_print("Title/SheetId reverse matches:", len(match_initial))
        
        # Look for sheetName / sheetId patterns inside JSON strings
        # E.g. \"title\":\"Data\",\"sheetId\":0
        # Wait, the double quotes in js variables might be escaped as \" or \\"
        properties = re.findall(r'\\"sheetId\\"\s*:\s*(\d+)\s*,\s*\\"title\\"\s*:\s*\\"([^\\"]+)\\"', html)
        my_print("Properties matches (sheetId/title):", len(properties))
        for sid, title in properties:
            my_print(f"  {title} -> {sid}")
            
        properties_rev = re.findall(r'\\"title\\"\s*:\s*\\"([^\\"]+)\\"\s*,\s*\\"sheetId\\"\s*:\s*(\d+)', html)
        my_print("Properties matches (title/sheetId):", len(properties_rev))
        for title, sid in properties_rev:
            my_print(f"  {title} -> {sid}")

        # Let's write the first 5000 chars of initialData to inspect if still empty
        for line in html.splitlines():
            if "_W_initialData" in line or "bootstrapData" in line:
                my_print("Found initial data line. Length:", len(line))
                my_print(line[:2000])
                break
                
except Exception as e:
    my_print("Error:", e)

with open("scratch/fetch_gids_output.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))
print("Done writing scratch/fetch_gids_output.txt")

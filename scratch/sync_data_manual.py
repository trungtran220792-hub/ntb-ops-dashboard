import urllib.request
import re
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

url = "https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/edit?gid=1365110988#gid=1365110988"
output_path = "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx"

print(f"Downloading from Google Sheets: {url}")
match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
if not match:
    print("Error: Invalid URL")
    sys.exit(1)

spreadsheet_id = match.group(1)
export_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=xlsx"

try:
    req = urllib.request.Request(
        export_url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        content = response.read()
        with open(output_path, 'wb') as f:
            f.write(content)
    print("Download successful!")
except Exception as e:
    print(f"Download error: {e}")

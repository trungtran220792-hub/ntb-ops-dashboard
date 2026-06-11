import urllib.request
import pandas as pd
import re

url = "https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit?gid=218211549#gid=218211549"
match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
if match:
    spreadsheet_id = match.group(1)
    export_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=xlsx"
    print(f"Downloading from {export_url}...")
    req = urllib.request.Request(
        export_url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        content = response.read()
        with open("scratch/temp_download.xlsx", "wb") as f:
            f.write(content)
    
    print("Reading sheet names...")
    with pd.ExcelFile("scratch/temp_download.xlsx") as xls:
        print("Sheet names:", xls.sheet_names)
else:
    print("No spreadsheet ID found")

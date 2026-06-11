import urllib.request
import pandas as pd
import re
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

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
        sheet_names = xls.sheet_names
        
        with open("scratch/sheets_info.txt", "w", encoding="utf-8") as out:
            out.write(f"Sheet names: {sheet_names}\n\n")
            for sheet in sheet_names:
                out.write(f"=== Sheet: {sheet} ===\n")
                try:
                    df = pd.read_excel(xls, sheet_name=sheet, nrows=5)
                    out.write(f"Columns: {list(df.columns)}\n")
                    out.write(df.to_string())
                    out.write("\n\n")
                except Exception as ex:
                    out.write(f"Error reading: {ex}\n\n")
                    
    print("Finished inspecting. Results written to scratch/sheets_info.txt")
else:
    print("No spreadsheet ID found")

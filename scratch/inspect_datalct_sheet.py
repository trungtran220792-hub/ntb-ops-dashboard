import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import re
import urllib.request

url = "https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit?gid=1469954076#gid=1469954076"
match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
spreadsheet_id = match.group(1)
export_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=xlsx"

print("Downloading Excel...")
req = urllib.request.Request(
    export_url,
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
)
with urllib.request.urlopen(req, timeout=60) as response:
    content = response.read()
    with open('downloaded_consolidated_sheet.xlsx', 'wb') as f:
        f.write(content)
print("Downloaded. Reading DataLTC sheet...")

df = pd.read_excel('downloaded_consolidated_sheet.xlsx', sheet_name='DataLTC', header=None)
print("DataLTC shape:", df.shape)
for i in range(15):
    print(f"Row {i}:", list(df.iloc[i].values))

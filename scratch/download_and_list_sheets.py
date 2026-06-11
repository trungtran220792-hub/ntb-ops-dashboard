import urllib.request
import pandas as pd
import openpyxl

url = "https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/export?format=xlsx"
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

print("Downloading sheet...")
try:
    with urllib.request.urlopen(req, timeout=30) as res:
        data = res.read()
    
    filename = "scratch/downloaded_consolidated_sheet.xlsx"
    with open(filename, "wb") as f:
        f.write(data)
    print(f"Saved to {filename}. Size: {len(data)} bytes")
    
    wb = openpyxl.load_workbook(filename, read_only=True)
    print("Sheets in workbook:")
    for name in wb.sheetnames:
        print(f"- {name}")
        
except Exception as e:
    print(f"Error: {e}")

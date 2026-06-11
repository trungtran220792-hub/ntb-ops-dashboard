import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
import json

excel_path = 'downloaded_consolidated_sheet.xlsx'
print("Loading excel file...")
xl = pd.ExcelFile(excel_path)
print("Sheet names:", xl.sheet_names)

for sheet in xl.sheet_names:
    if 'ltc' in sheet.lower():
        df = pd.read_excel(xl, sheet_name=sheet, nrows=5)
        print(f"\n--- {sheet} columns ---")
        for i, col in enumerate(df.columns):
            print(f"Index {i}: {col}")
        print("\nFirst 3 rows:")
        print(df.head(3).to_string())

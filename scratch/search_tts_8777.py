import pandas as pd
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Search OPR TTS.xlsx
file_path = "OPR TTS.xlsx"
if os.path.exists(file_path):
    xls = pd.ExcelFile(file_path)
    print("Sheets in OPR TTS.xlsx:", xls.sheet_names)
    for sheet in xls.sheet_names:
        print(f"Reading sheet: {sheet}")
        try:
            df = pd.read_excel(xls, sheet_name=sheet, nrows=10)
            print(f"  Columns: {list(df.columns)}")
        except Exception as e:
            print("  Error:", e)
else:
    print("OPR TTS.xlsx not found")

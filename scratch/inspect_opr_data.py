import openpyxl
import pandas as pd
import sys

wb_path = "scratch/downloaded_consolidated_sheet.xlsx"
wb = openpyxl.load_workbook(wb_path, read_only=True)

with open("scratch/opr_sheets_info.txt", "w", encoding="utf-8") as f:
    for name in ["OPR", "rawopr", "CoCauVung", "Data", "TTS", "DataLTC"]:
        if name in wb.sheetnames:
            f.write(f"\n=================== Sheet: {name} ===================\n")
            try:
                df = pd.read_excel(wb_path, sheet_name=name, nrows=5)
                f.write(f"Shape: {df.shape}\n")
                f.write(f"Columns: {list(df.columns)}\n")
                if not df.empty:
                    f.write(f"First row: {df.iloc[0].to_dict()}\n")
            except Exception as e:
                f.write(f"Error: {e}\n")
        else:
            f.write(f"Sheet {name} NOT found in workbook\n")
print("Done")

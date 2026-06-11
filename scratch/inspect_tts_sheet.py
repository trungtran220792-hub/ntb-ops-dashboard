import openpyxl
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    wb = openpyxl.load_workbook('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', read_only=True)
    print("Sheets in Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx:")
    for name in wb.sheetnames:
        print(f" - {name}")
except Exception as e:
    print("Error:", e)

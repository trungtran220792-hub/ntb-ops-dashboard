import openpyxl
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = 'Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx'
if os.path.exists(filepath):
    print(f"File {filepath} exists. Size: {os.path.getsize(filepath)} bytes.")
    wb = openpyxl.load_workbook(filepath, read_only=True)
    print("Sheets in workbook:", wb.sheetnames)
else:
    print(f"File {filepath} does not exist.")

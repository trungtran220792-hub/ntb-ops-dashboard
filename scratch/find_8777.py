import sys
import pandas as pd
import os

sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")

if os.path.exists(file_path):
    xls = pd.ExcelFile(file_path)
    print("Sheets in workbook:", xls.sheet_names)
    for sheet in xls.sheet_names:
        try:
            df = pd.read_excel(xls, sheet_name=sheet)
            for col in df.columns:
                try:
                    numeric_col = pd.to_numeric(df[col], errors='coerce')
                    matches = df[((numeric_col >= 0.8770) & (numeric_col <= 0.8785)) | ((numeric_col >= 87.70) & (numeric_col <= 87.85))]
                    if not matches.empty:
                        print(f"Match found in Sheet '{sheet}', Column '{col}':")
                        for idx, row in matches.iterrows():
                            # Print only a subset of columns to keep it clean
                            print(f"  Row {idx} in '{sheet}': Time={row.get('Time')}, % Gán={row.get('% Gán') or row.get('%Gán')}, Volume={row.get('Volume')}, Cấp={row.get('Cấp Quản Lý') or row.get('Cấp quản lý')}")
                except Exception as ex:
                    pass
        except Exception as e:
            print(f"Error reading sheet {sheet}: {e}")
else:
    print("File not found")

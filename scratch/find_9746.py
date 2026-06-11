import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")

if os.path.exists(file_path):
    xls = pd.ExcelFile(file_path)
    print("Sheets in workbook:", xls.sheet_names)
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        for col in df.columns:
            # Check if any value is close to 0.9746 or 97.46
            try:
                numeric_col = pd.to_numeric(df[col], errors='coerce')
                matches = df[((numeric_col >= 0.9745) & (numeric_col <= 0.9747)) | ((numeric_col >= 97.45) & (numeric_col <= 97.47))]
                if not matches.empty:
                    print(f"Match found in Sheet '{sheet}', Column '{col}':")
                    for idx, row in matches.iterrows():
                        print(f"  Row {idx}: {row.to_dict()}")
            except Exception as e:
                pass
else:
    print("File not found")

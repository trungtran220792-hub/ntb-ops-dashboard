import pandas as pd
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx"
if os.path.exists(file_path):
    xls = pd.ExcelFile(file_path)
    for sheet in xls.sheet_names:
        print(f"Reading sheet: {sheet}")
        try:
            df = pd.read_excel(xls, sheet_name=sheet)
            print(f"Columns in '{sheet}': {list(df.columns)}")
            for col in df.columns:
                # Let's search for 0.8777 or 87.77
                try:
                    num_col = pd.to_numeric(df[col], errors='coerce')
                    matches = df[(num_col >= 0.877) & (num_col <= 0.878)]
                    if not matches.empty:
                        print(f"  --> MATCH found in sheet '{sheet}', column '{col}':")
                        for idx, row in matches.iterrows():
                            print(f"    Row {idx}: {row.to_dict()}")
                except Exception as e:
                    pass
        except Exception as e:
            print(f"Error reading sheet {sheet}: {e}")
else:
    print("File not found")

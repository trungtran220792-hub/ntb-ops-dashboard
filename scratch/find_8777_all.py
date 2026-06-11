import sys
import pandas as pd
import os

sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"

for filename in os.listdir(workspace_dir):
    if filename.endswith(".xlsx") and filename != "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx":
        file_path = os.path.join(workspace_dir, filename)
        try:
            xls = pd.ExcelFile(file_path)
            for sheet in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet)
                for col in df.columns:
                    try:
                        numeric_col = pd.to_numeric(df[col], errors='coerce')
                        matches = df[((numeric_col >= 0.8770) & (numeric_col <= 0.8785)) | ((numeric_col >= 87.70) & (numeric_col <= 87.85))]
                        if not matches.empty:
                            print(f"Match found in File '{filename}', Sheet '{sheet}', Column '{col}':")
                            for idx, row in matches.iterrows():
                                print(f"  Row {idx}: {list(row.items())[:6]}")
                    except Exception:
                        pass
        except Exception as e:
            print(f"Error reading {filename}: {e}")

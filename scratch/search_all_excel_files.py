import os
import glob
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
excel_files = glob.glob(os.path.join(workspace_dir, "*.xlsx"))
print("Excel files in workspace:", [os.path.basename(f) for f in excel_files])

for file_path in excel_files:
    file_name = os.path.basename(file_path)
    print(f"\nSearching file: {file_name}")
    try:
        xls = pd.ExcelFile(file_path)
        for sheet in xls.sheet_names:
            try:
                # Read without header first to search everything
                df = pd.read_excel(xls, sheet_name=sheet, header=None)
                for r_idx, row in df.iterrows():
                    for c_idx, val in enumerate(row):
                        if val is not None:
                            try:
                                f_val = float(val)
                                if (0.8776 <= f_val <= 0.8778) or (87.76 <= f_val <= 87.78):
                                    print(f"  [{sheet}] Cell ({r_idx}, {c_idx}) = {f_val}")
                            except ValueError:
                                pass
            except Exception as e:
                print(f"  Error reading sheet {sheet}: {e}")
    except Exception as e:
        print(f"  Error reading file {file_name}: {e}")

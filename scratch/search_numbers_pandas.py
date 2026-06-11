import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

xls_path = "scratch/temp_download.xlsx"
targets = [1852, 957, 1098, 783, 1299, 1164, 608, 44209]

print("Loading sheets with pandas...")
# Read all sheets in the Excel file
xls = pd.ExcelFile(xls_path)
for sheet_name in xls.sheet_names:
    print(f"Checking sheet: {sheet_name}")
    try:
        df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
        # Search for targets in the values
        for r_idx, row in df.iterrows():
            for c_idx, val in enumerate(row):
                if pd.notna(val):
                    try:
                        val_num = float(val)
                        if any(abs(val_num - t) < 0.01 for t in targets):
                            print(f"MATCH: sheet='{sheet_name}', cell=({r_idx+1}, {c_idx+1}), val={val}")
                    except (ValueError, TypeError):
                        val_str = str(val)
                        if any(str(t) in val_str for t in targets):
                            print(f"MATCH (str): sheet='{sheet_name}', cell=({r_idx+1}, {c_idx+1}), val={val}")
    except Exception as e:
        print(f"Error checking sheet {sheet_name}: {e}")

print("Search done.")

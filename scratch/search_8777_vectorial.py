import os
import glob
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
excel_files = glob.glob(os.path.join(workspace_dir, "*.xlsx"))

for file_path in excel_files:
    file_name = os.path.basename(file_path)
    print(f"Scanning: {file_name}")
    try:
        xls = pd.ExcelFile(file_path)
        for sheet in xls.sheet_names:
            try:
                df = pd.read_excel(xls, sheet_name=sheet)
                for col in df.columns:
                    try:
                        num_col = pd.to_numeric(df[col], errors='coerce')
                        matches = df[(num_col >= 0.8776) & (num_col <= 0.8778)]
                        if not matches.empty:
                            print(f"  FOUND [0.8777] in sheet '{sheet}', col '{col}':")
                            print(matches.head(2).to_string())
                        matches_100 = df[(num_col >= 87.76) & (num_col <= 87.78)]
                        if not matches_100.empty:
                            print(f"  FOUND [87.77] in sheet '{sheet}', col '{col}':")
                            print(matches_100.head(2).to_string())
                    except Exception:
                        pass
            except Exception:
                pass
    except Exception as e:
        print(f"Error reading {file_name}: {e}")

print("Fast scan finished!")

import os
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

remaining_files = ["buu_cuc_bat_on.xlsx", "co_cau_ntb.xlsx", "off_tuyen_spe.xlsx", "Aging _5 ngày.xlsx", "Treo luân chuyển GIAO_TRẢ by IMTHIR.xlsx"]

for file_name in remaining_files:
    print(f"Scanning file: {file_name}")
    sys.stdout.flush()
    if not os.path.exists(file_name):
        print(f"  {file_name} does not exist.")
        continue
    try:
        xls = pd.ExcelFile(file_name)
        for sheet in xls.sheet_names:
            try:
                df = pd.read_excel(xls, sheet_name=sheet)
                for col in df.columns:
                    try:
                        num_col = pd.to_numeric(df[col], errors='coerce')
                        matches = df[(num_col >= 0.8776) & (num_col <= 0.8778)]
                        if not matches.empty:
                            print(f"    FOUND [0.8777] in sheet '{sheet}', col '{col}':")
                            print(matches.head(1).to_string())
                            sys.stdout.flush()
                        matches_100 = df[(num_col >= 87.76) & (num_col <= 87.78)]
                        if not matches_100.empty:
                            print(f"    FOUND [87.77] in sheet '{sheet}', col '{col}':")
                            print(matches_100.head(1).to_string())
                            sys.stdout.flush()
                    except Exception:
                        pass
            except Exception as e:
                print(f"    Error reading sheet {sheet}: {e}")
                sys.stdout.flush()
    except Exception as e:
        print(f"  Error loading file {file_name}: {e}")
        sys.stdout.flush()

print("Remaining scan finished!")

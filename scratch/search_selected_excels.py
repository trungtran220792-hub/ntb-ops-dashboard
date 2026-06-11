import os
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

def print_flush(msg):
    print(msg)
    sys.stdout.flush()

selected_files = ["Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx", "OPR TTS.xlsx", "temp_ops_check.xlsx"]

for file_name in selected_files:
    print_flush(f"Scanning file: {file_name}")
    if not os.path.exists(file_name):
        print_flush(f"  {file_name} does not exist.")
        continue
    try:
        xls = pd.ExcelFile(file_name)
        for sheet in xls.sheet_names:
            print_flush(f"  Reading sheet: {sheet}")
            try:
                df = pd.read_excel(xls, sheet_name=sheet)
                for col in df.columns:
                    try:
                        num_col = pd.to_numeric(df[col], errors='coerce')
                        matches = df[(num_col >= 0.8776) & (num_col <= 0.8778)]
                        if not matches.empty:
                            print_flush(f"    FOUND [0.8777] in sheet '{sheet}', col '{col}':")
                            print_flush(matches.head(2).to_string())
                        matches_100 = df[(num_col >= 87.76) & (num_col <= 87.78)]
                        if not matches_100.empty:
                            print_flush(f"    FOUND [87.77] in sheet '{sheet}', col '{col}':")
                            print_flush(matches_100.head(2).to_string())
                    except Exception:
                        pass
            except Exception as e:
                print_flush(f"    Error reading sheet {sheet}: {e}")
    except Exception as e:
        print_flush(f"  Error loading file {file_name}: {e}")

print_flush("Selected excels scan finished!")

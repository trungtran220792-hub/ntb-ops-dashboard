import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "sheet_names_fast.txt")

with open(output_path, "w", encoding="utf-8") as f:
    with pd.ExcelFile(file_path) as xls:
        f.write(f"Sheet names: {xls.sheet_names}\n")

print("Done writing sheet names.")

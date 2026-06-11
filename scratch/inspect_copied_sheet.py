import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "inspect_copied_sheet_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="DataLTC")
    f.write("DataLTC Columns:\n")
    f.write(str(list(df.columns)) + "\n\n")
    f.write("DataLTC Row 0-20:\n")
    f.write(df.head(20).to_string() + "\n")

print("Done inspect.")

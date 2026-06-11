import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "check_sync_progress_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df_raw = pd.read_excel(file_path, sheet_name="rawltc")
    df_data = pd.read_excel(file_path, sheet_name="DataLTC")
    
    # Strip columns
    df_raw.columns = [c.strip() for c in df_raw.columns]
    df_data.columns = [c.strip() for c in df_data.columns]
    
    # Filter rawltc for BC 158 and 2026-05-17
    f.write("=== rawltc rows for BC 158 and 2026-05-17 ===\n")
    raw_subset = df_raw[
        (df_raw['Chi tiết'].str.contains("BC 158", na=False)) & 
        (df_raw['Time'] == "2026-05-17 - Chủ Nhật")
    ]
    f.write(raw_subset.to_string() + "\n")
    f.write(f"Sum of Volume in rawltc: {raw_subset['Volume'].sum()}\n\n")
    
    # Filter DataLTC row 0
    f.write("=== DataLTC row 0 ===\n")
    f.write(str(df_data.iloc[0].to_dict()) + "\n")

print("Done trace.")

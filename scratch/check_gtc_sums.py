import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "check_gtc_sums.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df_raw = pd.read_excel(file_path, sheet_name="rawltc")
    df_raw.columns = [c.strip() for c in df_raw.columns]
    
    # BC 158 on 2026-05-30
    f.write("=== BC 158 on 2026-05-30 in rawltc ===\n")
    sub = df_raw[
        (df_raw['Chi tiết'].str.contains("BC 158", na=False)) & 
        (df_raw['Time'] == "2026-05-30 - Thứ 7")
    ]
    f.write(sub.to_string() + "\n")
    f.write(f"Volume sum: {sub['Volume'].sum()}\n\n")

print("Done check.")

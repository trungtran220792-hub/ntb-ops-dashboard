import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "inspect_data_sums_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    with pd.ExcelFile(file_path) as xls:
        # 1. Read Data (GTC)
        df_gtc = pd.read_excel(xls, sheet_name="Data")
        df_gtc.columns = [c.strip() for c in df_gtc.columns]
        f.write("=== Data (GTC) ===\n")
        f.write(f"Shape: {df_gtc.shape}\n")
        f.write(f"Columns: {list(df_gtc.columns)}\n")
        f.write(f"Unique Times: {list(df_gtc['Time'].dropna().unique()[:10])}\n\n")
        
        # 2. Read DataLTC
        df_ltc = pd.read_excel(xls, sheet_name="DataLTC")
        df_ltc.columns = [c.strip() for c in df_ltc.columns]
        f.write("=== DataLTC ===\n")
        f.write(f"Shape: {df_ltc.shape}\n")
        f.write(f"Columns: {list(df_ltc.columns)}\n")
        f.write(f"Unique Times: {list(df_ltc['Time'].dropna().unique()[:10])}\n\n")
        
        # 3. Read rawltc
        df_raw = pd.read_excel(xls, sheet_name="rawltc")
        df_raw.columns = [c.strip() for c in df_raw.columns]
        f.write("=== rawltc ===\n")
        f.write(f"Shape: {df_raw.shape}\n")
        f.write(f"Columns: {list(df_raw.columns)}\n")
        f.write(f"Unique Times: {list(df_raw['Time'].dropna().unique()[:10])}\n\n")

print("Done inspecting data sums.")

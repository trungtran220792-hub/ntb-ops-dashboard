import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "calculate_rawopr_vols_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="DataLTC")
    df.columns = [c.strip() for c in df.columns]
    
    latest_date = '2026-06-08 - Thứ 2'
    df_latest = df[df['Loại Hàng'] == latest_date].copy()
    
    # Let's convert columns to float
    df_latest['Time'] = pd.to_numeric(df_latest['Time'], errors='coerce').fillna(0)
    df_latest['% Gán'] = pd.to_numeric(df_latest['% Gán'], errors='coerce').fillna(0)
    df_latest['% LTC'] = pd.to_numeric(df_latest['% LTC'], errors='coerce').fillna(0)
    df_latest['Unnamed: 6'] = pd.to_numeric(df_latest['Unnamed: 6'], errors='coerce').fillna(0)
    
    # 1. Weighted average using '% Gán' column (which contains % LTC)
    # actual volume = Time column
    vol = df_latest['Time']
    ltc_vol_via_gan = vol * df_latest['% Gán']
    w_avg_gan = (ltc_vol_via_gan.sum() / vol.sum()) * 100 if vol.sum() > 0 else 0
    f.write(f"1. Weighted Average of % Gán (Actual % LTC): {w_avg_gan:.6f}%\n")
    
    # 2. Weighted average using '% LTC' column (which contains % LC)
    ltc_vol_via_ltc = vol * df_latest['% LTC']
    w_avg_ltc = (ltc_vol_via_ltc.sum() / vol.sum()) * 100 if vol.sum() > 0 else 0
    f.write(f"2. Weighted Average of % LTC (Actual % LC): {w_avg_ltc:.6f}%\n")
    
    # 3. Simple average of '% Gán' column
    f.write(f"3. Simple Average of % Gán column: {df_latest['% Gán'].mean() * 100:.6f}%\n")
    
    # 4. Simple average of '% LTC' column
    f.write(f"4. Simple Average of % LTC column: {df_latest['% LTC'].mean() * 100:.6f}%\n")
    
    # 5. What is the weighted average on rawltc sheet for the same date?
    df_raw = pd.read_excel(file_path, sheet_name="rawltc")
    df_raw.columns = [c.strip() for c in df_raw.columns]
    df_raw_latest = df_raw[df_raw['Time'] == latest_date].copy()
    
    raw_vol = df_raw_latest['Volume']
    raw_ltc = df_raw_latest['%LTC']
    w_avg_raw = ( (raw_vol * raw_ltc).sum() / raw_vol.sum() ) * 100 if raw_vol.sum() > 0 else 0
    f.write(f"5. Weighted Average on rawltc: {w_avg_raw:.6f}%\n")

print("Done calculate rawopr.")

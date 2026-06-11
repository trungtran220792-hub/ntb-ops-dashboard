import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "calculate_ltc_wtd_vols_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="DataLTC")
    df.columns = [c.strip() for c in df.columns]
    
    # Let's inspect latest date: 2026-06-08 - Thứ 2
    latest_date = '2026-06-08 - Thứ 2'
    df_latest = df[df['Loại Hàng'] == latest_date].copy() # remember 'Loại Hàng' is the actual date
    
    f.write(f"Latest Date: {latest_date}\n")
    f.write(f"Rows: {len(df_latest)}\n")
    
    # 1. Simple average of '% LTC' column
    df_latest['% LTC'] = pd.to_numeric(df_latest['% LTC'], errors='coerce').fillna(0)
    f.write(f"1. Simple Average of '% LTC' column: {df_latest['% LTC'].mean() * 100:.6f}%\n")
    
    # 2. Weighted average of '% LTC' using 'Time' column as volume
    df_latest['Time'] = pd.to_numeric(df_latest['Time'], errors='coerce').fillna(0)
    vol_time = df_latest['Time']
    ltc_vol_time = vol_time * df_latest['% LTC']
    w_avg_time = (ltc_vol_time.sum() / vol_time.sum()) * 100 if vol_time.sum() > 0 else 0
    f.write(f"2. Weighted Average of '% LTC' (Time = Vol): {w_avg_time:.6f}%\n")
    
    # 3. Simple average of 'Sản Lượng Lấy Thành Công' column
    df_latest['Sản Lượng Lấy Thành Công'] = pd.to_numeric(df_latest['Sản Lượng Lấy Thành Công'], errors='coerce').fillna(0)
    f.write(f"3. Simple Average of 'Sản Lượng Lấy Thành Công' column: {df_latest['Sản Lượng Lấy Thành Công'].mean() * 100:.6f}%\n")
    
    # 4. Weighted average of 'Sản Lượng Lấy Thành Công' using 'Time' as volume
    success_vol_time = vol_time * df_latest['Sản Lượng Lấy Thành Công']
    w_avg_success_time = (success_vol_time.sum() / vol_time.sum()) * 100 if vol_time.sum() > 0 else 0
    f.write(f"4. Weighted Average of 'Sản Lượng Lấy Thành Công' (Time = Vol): {w_avg_success_time:.6f}%\n")
    
    # 5. Let's check GTC metrics on 2026-06-08 - Thứ 2
    # Maybe 91.42% is the GTC percentage or something else?
    # No, they said: "sheet dataLTC cột %LTC nha"
    
    # 6. Wait! Let's check the date "2026-06-06 - Thứ 7"
    f.write("\n=== Testing for date: 2026-06-06 - Thứ 7 ===\n")
    df_06 = df[df['Loại Hàng'] == '2026-06-06 - Thứ 7'].copy()
    df_06['% LTC'] = pd.to_numeric(df_06['% LTC'], errors='coerce').fillna(0)
    df_06['Time'] = pd.to_numeric(df_06['Time'], errors='coerce').fillna(0)
    df_06['Sản Lượng Lấy Thành Công'] = pd.to_numeric(df_06['Sản Lượng Lấy Thành Công'], errors='coerce').fillna(0)
    
    f.write(f"1. Simple Average of '% LTC': {df_06['% LTC'].mean() * 100:.6f}%\n")
    ltc_vol_06 = df_06['Time'] * df_06['% LTC']
    w_avg_06 = (ltc_vol_06.sum() / df_06['Time'].sum()) * 100 if df_06['Time'].sum() > 0 else 0
    f.write(f"2. Weighted Average of '% LTC' (Time = Vol): {w_avg_06:.6f}%\n")
    
    # 7. Wait! Let's check the date "2026-06-05 - Thứ 6"
    f.write("\n=== Testing for date: 2026-06-05 - Thứ 6 ===\n")
    df_05 = df[df['Loại Hàng'] == '2026-06-05 - Thứ 6'].copy()
    df_05['% LTC'] = pd.to_numeric(df_05['% LTC'], errors='coerce').fillna(0)
    df_05['Time'] = pd.to_numeric(df_05['Time'], errors='coerce').fillna(0)
    
    f.write(f"1. Simple Average of '% LTC': {df_05['% LTC'].mean() * 100:.6f}%\n")
    ltc_vol_05 = df_05['Time'] * df_05['% LTC']
    w_avg_05 = (ltc_vol_05.sum() / df_05['Time'].sum()) * 100 if df_05['Time'].sum() > 0 else 0
    f.write(f"2. Weighted Average of '% LTC' (Time = Vol): {w_avg_05:.6f}%\n")

print("Done calculate search.")

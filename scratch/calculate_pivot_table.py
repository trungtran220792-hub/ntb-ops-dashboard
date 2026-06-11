import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "calculate_pivot_table_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="DataLTC")
    df.columns = [c.strip() for c in df.columns]
    
    latest_date = '2026-06-08 - Thứ 2'
    df_latest = df[df['Loại Hàng'] == latest_date].copy()
    
    f.write(f"=== Sums of columns in DataLTC for {latest_date} ===\n")
    for col in df_latest.columns:
        numeric_col = pd.to_numeric(df_latest[col], errors='coerce')
        f.write(f"{col} sum: {numeric_col.sum()}\n")
        f.write(f"{col} mean: {numeric_col.mean()}\n\n")
        
    # Test different division combinations
    # User said % LTC is 91.42%
    # Let's check some divisions
    f.write("=== Divisions ===\n")
    # 1. 'Sản Lượng Lấy Thành Công' sum / 'Sản Lượng Gán' sum
    sl_lay = pd.to_numeric(df_latest['Sản Lượng Lấy Thành Công'], errors='coerce').sum()
    sl_gan = pd.to_numeric(df_latest['Sản Lượng Gán'], errors='coerce').sum()
    f.write(f"Sản Lượng Lấy Thành Công sum / Sản Lượng Gán sum: {sl_lay / sl_gan * 100:.6f}%\n")
    
    # 2. 'Sản Lượng Lấy Thành Công' sum / 'Volume' sum (wait, Volume column has `% Gán` values)
    vol_col = pd.to_numeric(df_latest['Volume'], errors='coerce').sum()
    f.write(f"Sản Lượng Lấy Thành Công sum / Volume column sum: {sl_lay / vol_col * 100:.6f}%\n")
    
    # 3. What if we sum the actual volumes?
    # Actual Volume is in 'Time' column
    act_vol = pd.to_numeric(df_latest['Time'], errors='coerce').sum()
    # Actual success is: Actual_Volume * Actual_LTC_Pct?
    # Wait, in rawltc, let's check:
    # 'Sản Lượng Lấy Thành Công' in DataLTC is column 9. Let's see if we multiply actual volume by % LTC
    df_latest['Actual_LTC_Pct'] = pd.to_numeric(df_latest['% LTC'], errors='coerce').fillna(0)
    df_latest['Actual_Volume'] = pd.to_numeric(df_latest['Time'], errors='coerce').fillna(0)
    act_success = (df_latest['Actual_Volume'] * df_latest['Actual_LTC_Pct']).sum()
    f.write(f"Actual LTC Volume (Actual_Volume * % LTC) sum: {act_success}\n")
    f.write(f"Actual Volume (Time column) sum: {act_vol}\n")
    f.write(f"Weighted LTC (Actual LTC Volume / Actual Volume): {act_success / act_vol * 100:.6f}%\n")
    
    # 4. What about other dates?
    # Let's find any date where weighted average or some division is 91.42%
    f.write("\n=== Scanning all dates for 91.42% combinations ===\n")
    for d in df['Loại Hàng'].dropna().unique():
        df_d = df[df['Loại Hàng'] == d]
        df_d_ltc = pd.to_numeric(df_d['% LTC'], errors='coerce').fillna(0)
        df_d_time = pd.to_numeric(df_d['Time'], errors='coerce').fillna(0)
        
        # Weighted % LTC
        w_ltc = (df_d_time * df_d_ltc).sum() / df_d_time.sum() * 100 if df_d_time.sum() > 0 else 0
        
        # Simple average of % LTC
        avg_ltc = df_d_ltc.mean() * 100
        
        if (91.40 <= w_ltc <= 91.45) or (91.40 <= avg_ltc <= 91.45):
            f.write(f"Match on {d}: Weighted LTC = {w_ltc:.4f}%, Simple Avg LTC = {avg_ltc:.4f}%\n")
            
        # What if it's rawltc?
        # Let's look up rawltc for date d
        # rawltc date matching d
        # Let's check rawltc weighted % LTC

print("Done calculate pivot.")

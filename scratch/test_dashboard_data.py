import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "test_mapping_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    with pd.ExcelFile(file_path) as xls:
        sheet_names_lower = [s.lower() for s in xls.sheet_names]
        idx = sheet_names_lower.index('dataltc')
        df = pd.read_excel(xls, sheet_name=xls.sheet_names[idx])
        df.columns = [c.strip() for c in df.columns]
        
        rename_map = {
            'Loại Hàng': 'Time',
            'Time': 'Volume',
            'Volume': '% Gán',
            '% Gán': '%LTC',
            '% LTC': '%LC'
        }
        df = df.rename(columns=rename_map)
        
        f.write(f"Mapped columns: {list(df.columns)}\n")
        
        df = df.dropna(subset=["Volume"]).copy()
        df['Leadtime'] = pd.to_numeric(df['Leadtime'], errors='coerce')
        df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce').fillna(0)
        df['%LTC'] = pd.to_numeric(df['%LTC'], errors='coerce').fillna(0)
        df['ltc_vol'] = df['Volume'] * df['%LTC']
        
        times = df['Time'].dropna().unique()
        dates_sorted = sorted(times, key=lambda x: pd.to_datetime(str(x).split(' - ')[0]))
        latest_date_ltc = dates_sorted[-1]
        
        df_ltc_latest = df[df['Time'] == latest_date_ltc]
        
        total_ltc_vol = float(df_ltc_latest['Volume'].sum())
        total_on_ltc_vol = float(df_ltc_latest['ltc_vol'].sum())
        overall_ltc = total_on_ltc_vol / total_ltc_vol if total_ltc_vol > 0 else 0
        
        f.write(f"Latest Date: {latest_date_ltc}\n")
        f.write(f"Total Vol: {total_ltc_vol}\n")
        f.write(f"Overall LTC Pct: {overall_ltc * 100:.4f}%\n")

print("Done verify.")

import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

xls_path = "scratch/temp_download.xlsx"
sheets = ['Data', 'TTS', 'DataLTC', 'shopee_tiktok']

targets = {
    # Name from screenshot: Volume target
    "56 Phan": [1852, 957],
    "115 Lý Nam Đế": [1098],
    "575 Đường 8/4": [783],
    "40A Yết Kiêu": [1299],
    "466 Đường 23/10": [1164],
    "309 Đường 8/4": [608]
}

for sheet in sheets:
    print(f"\n=== Checking Sheet: {sheet} ===")
    df = pd.read_excel(xls_path, sheet_name=sheet)
    
    # Identify date and volume columns
    date_col = next((c for c in df.columns if "time" in c.lower() or "date" in c.lower()), None)
    vol_col = next((c for c in df.columns if "volume" in c.lower() or "vol" in c.lower()), None)
    po_col = next((c for c in df.columns if "chi tiết" in c.lower() or "bưu cục" in c.lower() or "warehouse_name" in c.lower()), None)
    
    if not date_col or not vol_col or not po_col:
        print(f"Skipping {sheet} due to missing columns: date={date_col}, vol={vol_col}, po={po_col}")
        continue
        
    num_dates = len(df[date_col].unique())
    print(f"Number of unique dates: {num_dates}")
    
    # Calculate average volume
    po_avg = df.groupby(po_col)[vol_col].sum() / num_dates
    
    # Print matching for our targets
    for name, expected_vals in targets.items():
        matches = [po for po in po_avg.index if name.lower() in str(po).lower()]
        for po in matches:
            val = po_avg[po]
            print(f"  {po}: {val:.2f} (Expected one of {expected_vals})")
            
# Let's also check if there is an exact sheet we missed
# E.g. 'CoCauVung' sheet is ['warehouse_id', 'Bưu cục', 'Tỉnh', 'AM']
# What about other sheets?

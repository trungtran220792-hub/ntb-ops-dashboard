import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    df = pd.read_excel('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', sheet_name='Sheet13')
    latest = '2026-06-08 - Thứ 2'
    df_latest = df[df['Time'] == latest]
    print(f"Total rows in Sheet13 for {latest}: {len(df_latest)}")
    
    # Calculate Gán and Volume sum
    # Wait, does Sheet13 have % Gán column? Let's check how % Gán values look (decimal or percentage)
    print("First 5 rows of Sheet13 for latest date:")
    print(df_latest.head(5).to_string())
    
    df_latest['% Gán'] = pd.to_numeric(df_latest['% Gán'], errors='coerce')
    df_latest['Volume'] = pd.to_numeric(df_latest['Volume'], errors='coerce')
    
    vol_sum = df_latest['Volume'].sum()
    # Let's calculate weighted assign rate.
    # Note: % Gán in Sheet13 might be stored as percentage (e.g. 87.77 or 0.8777). 
    # Let's check the values first. If they are e.g. 0.95, it's decimal.
    assigned_vol = (df_latest['Volume'] * df_latest['% Gán']).sum()
    weighted_rate = assigned_vol / vol_sum * 100 if vol_sum > 0 else 0
    print(f"Volume sum: {vol_sum}")
    print(f"Assigned Volume (if % Gán is decimal): {assigned_vol}")
    print(f"Weighted Rate: {weighted_rate:.6f}%")
    
    # What if % Gán is already a percentage?
    # Let's print unique values in % Gán to see:
    print("Unique % Gán values in latest date:", df_latest['% Gán'].unique()[:10])
except Exception as e:
    print("Error:", e)

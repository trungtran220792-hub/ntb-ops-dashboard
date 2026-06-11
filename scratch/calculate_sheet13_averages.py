import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    df = pd.read_excel('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', sheet_name='Sheet13')
    latest = '2026-06-08 - Thứ 2'
    df_latest = df[df['Time'] == latest]
    
    # Calculate different averages
    print("Sheet13 - Simple average of % Gán:", df_latest['% Gán'].mean() * 100)
    print("Sheet13 - Weighted average of % Gán:", (df_latest['Volume'] * df_latest['% Gán']).sum() / df_latest['Volume'].sum() * 100)
    
    # By Jenis Hàng (Loại Hàng)
    for name, group in df_latest.groupby('Loại Hàng'):
        vol = group['Volume'].sum()
        assigned = (group['Volume'] * group['% Gán']).sum()
        rate = assigned / vol * 100 if vol > 0 else 0
        print(f"Loại Hàng {name}: weighted_rate={rate:.4f}%, simple_rate={group['% Gán'].mean()*100:.4f}%")
        
except Exception as e:
    print("Error:", e)

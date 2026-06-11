import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    df_gtc = pd.read_excel('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', sheet_name='Data')
    latest = '2026-06-08 - Thứ 2'
    df_latest = df_gtc[df_gtc['Time'] == latest].copy()
    
    # Calculate Gán and Volume for each Post Office (Chi tiết)
    po_data = df_latest.groupby('Chi tiết').agg({'Volume': 'sum', 'Sản Lượng Gán': 'sum'}).reset_index()
    
    # Filter by different Volume thresholds and check the overall weighted assign rate
    for threshold in [0, 50, 100, 150, 200, 300, 500]:
        filtered_po = po_data[po_data['Volume'] >= threshold]
        vol_sum = filtered_po['Volume'].sum()
        gan_sum = filtered_po['Sản Lượng Gán'].sum()
        rate = gan_sum / vol_sum * 100 if vol_sum > 0 else 0
        print(f"Threshold >= {threshold}: Vol={vol_sum}, Gán={gan_sum}, %Gán={rate:.4f}%")
        
    # What if we filter the raw rows of df_latest directly?
    for threshold in [0, 10, 50, 100]:
        filtered_df = df_latest[df_latest['Volume'] >= threshold]
        vol_sum = filtered_df['Volume'].sum()
        gan_sum = filtered_df['Sản Lượng Gán'].sum()
        rate = gan_sum / vol_sum * 100 if vol_sum > 0 else 0
        print(f"Row threshold >= {threshold}: Vol={vol_sum}, Gán={gan_sum}, %Gán={rate:.4f}%")
        
except Exception as e:
    print("Error:", e)

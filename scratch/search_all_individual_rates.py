import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    df_gtc = pd.read_excel('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', sheet_name='Data')
    latest = '2026-06-08 - Thứ 2'
    df_latest = df_gtc[df_gtc['Time'] == latest]
    
    print("--- POST OFFICE INDIVIDUAL % GÁN ---")
    for idx, row in df_latest.iterrows():
        p_name = row['Chi tiết']
        vol = row['Volume']
        gan = row['Sản Lượng Gán']
        rate = (gan / vol * 100) if vol > 0 else 0
        if 87.7 <= rate <= 87.85:
            print(f"  {p_name}: Vol={vol}, Gán={gan}, Rate={rate:.4f}%")
            
except Exception as e:
    print("Error:", e)

import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    df_gtc = pd.read_excel('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', sheet_name='Data')
    df_ltc = pd.read_excel('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', sheet_name='DataLTC')
    df_bc = pd.read_excel('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', sheet_name='Bưu cục', header=1)
    
    latest = '2026-06-08 - Thứ 2'
    
    g_latest = df_gtc[df_gtc['Time'] == latest]
    l_latest = df_ltc[df_ltc['Time'] == latest]
    bc_latest = df_bc[df_bc['Time'] == latest]
    
    print("DATA SHEET:")
    print("  Simple average of % Gán:", g_latest['% Gán'].mean() * 100)
    print("  Weighted average of % Gán:", (g_latest['Sản Lượng Gán'].sum() / g_latest['Volume'].sum()) * 100)
    
    print("\nDATALTC SHEET:")
    print("  Simple average of %Gán:", l_latest['%Gán'].mean() * 100)
    print("  Weighted average of %Gán:", (l_latest['Sản Lượng Gán'].sum() / l_latest['Volume'].sum()) * 100)
    
    print("\nBƯU CỤC SHEET:")
    print("  Simple average of %Gán:", bc_latest['%Gán'].mean() * 100)
    print("  Weighted average of %Gán:", (bc_latest['Gán'].sum() / bc_latest['Volume'].sum()) * 100)
    
    # Let's search if there's any specific column in Bưu cục sheet that has 87.77% on latest date
    # Bưu cục columns: ['%Gán', '%Chưa Gán', '%GTC', '%Chuyển trả', '%Tồn']
    print("\nBưu cục averages:")
    for col in ['%Gán', '%Chưa Gán', '%GTC', '%Chuyển trả', '%Tồn']:
        if col in bc_latest.columns:
            print(f"  {col}: simple_avg={bc_latest[col].mean()*100:.4f}%, weighted_avg={( (bc_latest[col]*bc_latest['Volume']).sum() / bc_latest['Volume'].sum() )*100:.4f}%")
            
except Exception as e:
    print("Error:", e)

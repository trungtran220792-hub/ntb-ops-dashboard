import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    df = pd.read_excel('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', sheet_name='Data')
    print("--- DATA SHEET DAILY OVERALL % GÁN ---")
    for date, group in df.groupby('Time'):
        vol = group['Volume'].sum()
        gan = group['Sản Lượng Gán'].sum()
        print(f"{date}: Vol={vol}, Gán={gan}, %Gán={gan/vol*100:.4f}%")
        
    print("\n--- DATALTC SHEET DAILY OVERALL % GÁN ---")
    df_ltc = pd.read_excel('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', sheet_name='DataLTC')
    for date, group in df_ltc.groupby('Time'):
        vol = group['Volume'].sum()
        gan = group['Sản Lượng Gán'].sum()
        print(f"{date}: Vol={vol}, Gán={gan}, %Gán={gan/vol*100:.4f}%")
except Exception as e:
    print("Error:", e)

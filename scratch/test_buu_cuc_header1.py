import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    df = pd.read_excel('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', sheet_name='Bưu cục', header=1)
    print("Columns:", list(df.columns))
    print("First 3 rows:")
    print(df.iloc[:3, :15].to_string())
    
    # Calculate Gán and Volume sum for 2026-06-08 - Thứ 2
    latest = '2026-06-08 - Thứ 2'
    df_latest = df[df['Time'] == latest]
    print(f"Number of rows for {latest}: {len(df_latest)}")
    vol = df_latest['Volume'].sum()
    gan = df_latest['Gán'].sum()
    print('Bưu cục Vol:', vol)
    print('Bưu cục Gán:', gan)
    if vol > 0:
        print('Bưu cục % Gán (weighted):', gan / vol * 100)
    else:
        print('Vol is 0')
except Exception as e:
    print("Error:", e)

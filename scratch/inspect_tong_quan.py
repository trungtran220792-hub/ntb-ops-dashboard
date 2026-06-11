import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    df = pd.read_excel('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', sheet_name='Tổng quan')
    print("Columns:", list(df.columns))
    print(df.iloc[:30, :10].to_string())
except Exception as e:
    print("Error:", e)

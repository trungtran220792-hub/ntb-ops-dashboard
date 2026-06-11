import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', sheet_name='Bưu cục', nrows=10)
for idx, row in df.iterrows():
    print(f"Row {idx}: {list(row)}")

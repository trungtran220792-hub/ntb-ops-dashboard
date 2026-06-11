import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd

df = pd.read_csv('ops_ltc.csv')
print("Columns in ops_ltc.csv:")
print(df.columns.tolist())

print("\nSample rows:")
cols_to_show = ['Chi tiết', 'Time', 'Volume', '%LTC', 'Sản Lượng Lấy Thành Công', 'Sản Lượng Gán', 'Tỉnh']
print(df[cols_to_show].head(10).to_string())

print("\nData types:")
print(df[cols_to_show].dtypes)

# Check unique values in %LTC
print("\nUnique values in %LTC (first 20):")
print(df['%LTC'].unique()[:20])

# Check unique values in Sản Lượng Lấy Thành Công
print("\nUnique values in Sản Lượng Lấy Thành Công (first 20):")
print(df['Sản Lượng Lấy Thành Công'].unique()[:20])

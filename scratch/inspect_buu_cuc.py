import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', sheet_name='Bưu cục')
print(df.iloc[:40, :16].to_string())

import sys
import os
sys.path.append(os.getcwd())
sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd

path_aging = 'Aging _5 ngày.xlsx'
if os.path.exists(path_aging):
    with pd.ExcelFile(path_aging) as xls:
        df = pd.read_excel(xls, sheet_name="Đơn giao aging trên 5 ngày", nrows=5)
        print("Aging sheet columns:")
        print(df.columns.tolist())
        print(df.head(2))

path_treo = 'Treo luân chuyển GIAO_TRẢ by IMTHIR.xlsx'
if os.path.exists(path_treo):
    with pd.ExcelFile(path_treo) as xls:
        df = pd.read_excel(xls, sheet_name="stuck", nrows=5)
        print("\nTreo sheet columns:")
        print(df.columns.tolist())
        print(df.head(2))

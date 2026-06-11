import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import os

if os.path.exists('ops_ltc.csv'):
    df = pd.read_csv('ops_ltc.csv')
    print("Columns:", list(df.columns))
    print(df.head(10))
else:
    print("ops_ltc.csv does not exist.")

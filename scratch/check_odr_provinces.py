import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

df_odr = pd.read_csv('ODR TTS.csv')
print("Unique values of 'Quản lý' in ODR TTS.csv:")
for v in df_odr['Quản lý'].dropna().unique():
    print(f"  - '{v}'")

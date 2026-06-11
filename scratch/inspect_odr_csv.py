import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    df = pd.read_csv('ODR TTS.csv')
    print("Columns in 'ODR TTS.csv':", list(df.columns))
    print("\nFirst 10 rows:")
    print(df.head(10).to_string())
except Exception as e:
    print("Error:", e)

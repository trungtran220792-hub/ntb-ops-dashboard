import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import os

if os.path.exists('ODR TTS.csv'):
    df = pd.read_csv('ODR TTS.csv')
    print("Columns:", list(df.columns))
    print(df.head(10))
else:
    print("ODR TTS.csv does not exist.")

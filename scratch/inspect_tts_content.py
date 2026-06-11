import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    df = pd.read_excel('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', sheet_name='TTS')
    print("TTS Sheet Columns:", df.columns.tolist())
    print("\nTTS Sheet Shape:", df.shape)
    print("\nTTS Sheet First 10 rows:")
    print(df.head(10).to_string())
except Exception as e:
    print("Error:", e)

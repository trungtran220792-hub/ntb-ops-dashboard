import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    df = pd.read_csv('ODR TTS.csv')
    print("Unique dates in CSV:", df['Time'].unique()[:10])
    
    # Parse GTC and %Ontime
    df['GTC'] = pd.to_numeric(df['GTC'], errors='coerce')
    df['%Ontime'] = pd.to_numeric(df['%Ontime'].astype(str).str.replace(',', '.').str.rstrip('%'), errors='coerce') / 100
    df['ontime_vol'] = df['GTC'] * df['%Ontime']
    
    # Let's calculate daily overall ontime
    print("\n--- ODR DAILY OVERALL RATE ---")
    for date, group in df.groupby('Time'):
        gtc_sum = group['GTC'].sum()
        ontime_sum = group['ontime_vol'].sum()
        rate = ontime_sum / gtc_sum * 100 if gtc_sum > 0 else 0
        if '2026-06-08' in date or '2026-06-07' in date:
            print(f"{date}: GTC={gtc_sum}, Ontime={ontime_sum}, ODR={rate:.4f}%")
except Exception as e:
    print("Error:", e)

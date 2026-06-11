import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    df_odr = pd.read_csv('ODR TTS.csv')
    df_odr['GTC'] = pd.to_numeric(df_odr['GTC'], errors='coerce')
    df_odr['%Ontime'] = pd.to_numeric(df_odr['%Ontime'].astype(str).str.replace(',', '.').str.rstrip('%'), errors='coerce') / 100
    df_odr['ontime_vol'] = df_odr['GTC'] * df_odr['%Ontime']
    
    trend_odr = df_odr.groupby('Time').agg({'GTC': 'sum', 'ontime_vol': 'sum'}).reset_index()
    trend_odr['% ODR'] = (trend_odr['ontime_vol'] / trend_odr['GTC']) * 100
    trend_odr_list = trend_odr.sort_values('Time').to_dict(orient='records')
    
    print("Trend ODR first 5 entries:")
    print(trend_odr_list[:5])
    print("Trend ODR last 5 entries:")
    print(trend_odr_list[-5:])
    
except Exception as e:
    print("Error:", e)

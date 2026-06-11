import os
import pandas as pd
import sys

# Reconfigure stdout to use UTF-8 to avoid encoding errors on Windows console
sys.stdout.reconfigure(encoding='utf-8')

print("=== CHECKING ODR TTS DATA ===")

odr_path = 'ODR TTS.csv'
if os.path.exists(odr_path):
    print("ODR TTS.csv exists.")
    df_odr = pd.read_csv(odr_path)
    print("ODR CSV columns:", df_odr.columns.tolist())
    print("ODR CSV size:", len(df_odr))
    print("ODR CSV unique dates (Time):", df_odr['Time'].dropna().unique().tolist()[:10])
    
    # Try parsing ODR TTS.csv like app.py does
    try:
        df_odr['GTC'] = pd.to_numeric(df_odr['GTC'], errors='coerce')
        df_odr['%Ontime'] = pd.to_numeric(df_odr['%Ontime'].astype(str).str.replace(',', '.').str.rstrip('%'), errors='coerce') / 100
        df_odr['ontime_vol'] = df_odr['GTC'] * df_odr['%Ontime']
        print("Successfully parsed ODR values.")
        print("Total GTC in ODR:", df_odr['GTC'].sum())
        print("Total ontime volume:", df_odr['ontime_vol'].sum())
    except Exception as e:
        print("Error parsing ODR CSV:", e)
else:
    print("ODR TTS.csv does not exist!")

print("\n=== CHECKING OPERATIONAL CACHE/DF ===")
# Let's inspect the cached pickle file for Báo cáo vận hành (specifically tts or gtc) to see the dates
gtc_cache = '.cache_Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx_gtc.pkl'
if os.path.exists(gtc_cache):
    df_gtc = pd.read_pickle(gtc_cache)
    print("GTC cache columns:", df_gtc.columns.tolist())
    print("GTC cache unique dates (Time):", df_gtc['Time'].dropna().unique().tolist()[:10])
    
    # Check max date
    times = df_gtc['Time'].dropna().unique()
    try:
        dates_sorted = sorted(times, key=lambda x: pd.to_datetime(str(x).split(' - ')[0]))
        latest_date_gtc = dates_sorted[-1] if dates_sorted else None
        print("Latest date GTC (sorted):", latest_date_gtc)
        if latest_date_gtc:
            # Check if this latest date is in ODR
            if os.path.exists(odr_path):
                df_latest_odr = df_odr[df_odr['Time'] == latest_date_gtc]
                print(f"ODR rows matching latest date ({latest_date_gtc}):", len(df_latest_odr))
                if not df_latest_odr.empty:
                    print("Sample rows:")
                    print(df_latest_odr.head(2))
    except Exception as e:
        print("Error sorting GTC dates:", e)
else:
    print("GTC cache file not found!")

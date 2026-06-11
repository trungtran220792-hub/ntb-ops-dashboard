import pandas as pd
import os

odr_path = 'ODR TTS.csv'
if os.path.exists(odr_path):
    try:
        df_odr = pd.read_csv(odr_path)
        df_odr['GTC'] = pd.to_numeric(df_odr['GTC'], errors='coerce')
        
        # Chatbot logic:
        # df_odr['%Ontime'] = pd.to_numeric(df_odr['%Ontime'].astype(str).str.rstrip('%'), errors='coerce') / 100
        # Let's see what happens:
        df_odr['%Ontime_no_replace'] = pd.to_numeric(df_odr['%Ontime'].astype(str).str.rstrip('%'), errors='coerce') / 100
        df_odr['%Ontime_with_replace'] = pd.to_numeric(df_odr['%Ontime'].astype(str).str.replace(',', '.').str.rstrip('%'), errors='coerce') / 100
        
        print("First few rows of raw %Ontime:")
        print(df_odr['%Ontime'].head())
        print("\nParsed without replace:")
        print(df_odr['%Ontime_no_replace'].head())
        print("\nParsed with replace:")
        print(df_odr['%Ontime_with_replace'].head())
        
        print("\nNaN count without replace:", df_odr['%Ontime_no_replace'].isna().sum())
        print("NaN count with replace:", df_odr['%Ontime_with_replace'].isna().sum())
        
        # Test the sum and product
        df_odr['ontime_vol'] = df_odr['GTC'] * df_odr['%Ontime_no_replace']
        latest_date = df_odr['Time'].max()
        df_latest = df_odr[df_odr['Time'] == latest_date]
        if not df_latest.empty:
            overall_odr = (df_latest['ontime_vol'].sum() / df_latest['GTC'].sum()) * 100
            print(f"\nOverall ODR (chatbot logic) for {latest_date}: {overall_odr}%")
    except Exception as e:
        print("Error during simulation:", e)
else:
    print("ODR CSV not found.")

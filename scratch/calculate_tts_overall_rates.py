import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    df = pd.read_excel('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', sheet_name='TTS')
    
    # Let's clean the columns
    df = df.dropna(subset=['Volume']).copy()
    df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
    df['% Gán'] = pd.to_numeric(df['% Gán'], errors='coerce')
    df['assigned_vol'] = df['Volume'] * df['% Gán']
    
    df['% GTC'] = pd.to_numeric(df['% GTC'], errors='coerce')
    df['delivered_vol'] = df['Volume'] * df['% GTC']
    
    print("TTS Sheet daily summary:")
    # Sort dates
    times = df['Time'].dropna().unique()
    dates_sorted = sorted(times, key=lambda x: pd.to_datetime(str(x).split(' - ')[0]))
    
    for date in dates_sorted:
        df_date = df[df['Time'] == date]
        vol_sum = df_date['Volume'].sum()
        assigned_sum = df_date['assigned_vol'].sum()
        delivered_sum = df_date['delivered_vol'].sum()
        
        assign_rate = assigned_sum / vol_sum * 100 if vol_sum > 0 else 0
        gtc_rate = delivered_sum / vol_sum * 100 if vol_sum > 0 else 0
        
        print(f"Date: {date} | Total Vol: {vol_sum} | Assigned Vol: {assigned_sum:.2f} | Assign Rate: {assign_rate:.2f}% | GTC Rate: {gtc_rate:.2f}%")
        
except Exception as e:
    print("Error:", e)

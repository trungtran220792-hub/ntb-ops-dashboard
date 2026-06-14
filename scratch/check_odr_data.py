import pandas as pd
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Helper to normalize %
def normalize_pct_col(series):
    def convert(val):
        if pd.isna(val):
            return 0.0
        s = str(val).strip().replace('%', '').replace(',', '.')
        try:
            return float(s) / 100.0
        except:
            return 0.0
    return series.apply(convert)

def get_compare_deltas(trend, val_key):
    if not trend or len(trend) < 2:
        return {'n1': 0.0, 'wk': 0.0}
    
    # Sort trend by date
    # Format of Time: 'YYYY-MM-DD - Thứ X'
    try:
        trend = sorted(trend, key=lambda x: pd.to_datetime(str(x['Time']).split(' - ')[0]))
    except Exception as e:
        print("Error sorting trend:", e)
        
    latest = trend[-1]
    latest_val = latest.get(val_key, 0.0)
    
    n1_val = 0.0
    if len(trend) >= 2:
        n1_val = trend[-2].get(val_key, 0.0)
        
    wk_val = 0.0
    # Match same day of week (split splitting 'Thứ X')
    latest_dow = str(latest['Time']).split(' - ')[-1] if ' - ' in str(latest['Time']) else None
    if latest_dow:
        for item in reversed(trend[:-1]):
            dow = str(item['Time']).split(' - ')[-1] if ' - ' in str(item['Time']) else None
            if dow == latest_dow:
                wk_val = item.get(val_key, 0.0)
                break
                
    return {
        'n1': latest_val - n1_val if latest_val is not None and n1_val is not None else 0.0,
        'wk': latest_val - wk_val if latest_val is not None and wk_val is not None else 0.0
    }

# Read data
df_gtc = pd.read_csv('ops_gtc.csv')
df_odr = pd.read_csv('ODR TTS.csv')

df_gtc['Volume'] = pd.to_numeric(df_gtc['Volume'], errors='coerce')
df_gtc['% GTC'] = normalize_pct_col(df_gtc['% GTC'])
df_gtc['delivered_vol'] = df_gtc['Volume'] * df_gtc['% GTC']

df_odr.columns = [str(c).strip() for c in df_odr.columns]
df_odr['GTC'] = pd.to_numeric(df_odr['GTC'], errors='coerce')
ontime_col = next((c for c in df_odr.columns if c.lower() in ['%ontime', '% ontime', '%on time', '% on time']), '%Ontime')
df_odr['%Ontime'] = normalize_pct_col(df_odr[ontime_col])
df_odr['ontime_vol'] = df_odr['GTC'] * df_odr['%Ontime']

# Calculate trends
trend_odr = df_odr.groupby('Time').agg({'GTC': 'sum', 'ontime_vol': 'sum'}).reset_index()
trend_odr['% ODR'] = (trend_odr['ontime_vol'] / trend_odr['GTC']) * 100
trend_odr_list = trend_odr.sort_values('Time').to_dict(orient='records')

for test_date in ['2026-06-12 - Thứ 6', '2026-06-13 - Thứ 7']:
    print(f"\n=== Testing Date: {test_date} ===")
    
    # overall_odr_tts
    df_latest_odr = df_odr[df_odr['Time'] == test_date]
    overall_odr_tts = None
    if not df_latest_odr.empty:
        gtc_sum_odr = df_latest_odr['GTC'].sum()
        ontime_sum_odr = df_latest_odr['ontime_vol'].sum()
        overall_odr_tts = round(ontime_sum_odr / gtc_sum_odr * 100, 2) if gtc_sum_odr > 0 else 0.0
    
    print("overall_odr_tts:", overall_odr_tts)
    
    # Trend up to selected date
    # (If frontend filter is applied, trend is filtered up to selected date)
    test_dt = pd.to_datetime(test_date.split(' - ')[0])
    filtered_trend = [
        item for item in trend_odr_list
        if pd.to_datetime(str(item['Time']).split(' - ')[0]) <= test_dt
    ]
    
    deltas = get_compare_deltas(filtered_trend, '% ODR')
    print("Compare Deltas:", deltas)

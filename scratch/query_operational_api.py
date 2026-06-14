import requests
import json
import sys

# Configure stdout/stderr to use UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

try:
    # Query with default (latest date)
    r = requests.get('http://127.0.0.1:5000/api/operational')
    data = r.json()
    print("=== Operational API (default) ===")
    print("overall_odr_tts:", data.get("overall_odr_tts"))
    
    trend_odr = data.get("trend_odr", [])
    print("trend_odr length:", len(trend_odr))
    if len(trend_odr) > 0:
        print("Last 3 trend entries:")
        for entry in trend_odr[-3:]:
            print("  ", entry)
            
    # Query with specific dates
    for date in ["2026-06-12 - Thứ 6", "2026-06-13 - Thứ 7"]:
        r2 = requests.get(f'http://127.0.0.1:5000/api/operational?date={date}')
        data2 = r2.json()
        print(f"\n=== Operational API for {date} ===")
        print("overall_odr_tts:", data2.get("overall_odr_tts"))

except Exception as e:
    print("Error querying API:", e)

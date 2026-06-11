import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_url = 'http://127.0.0.1:5000'
auth = ('admin', 'admin123')
date_param = "2026-06-09+-+Thứ+3"

url = f"{base_url}/api/summary-dashboard?date={date_param}&time_group=ngay"
res = requests.get(url, auth=auth)
if res.status_code == 200:
    data = res.json()
    print("=== /api/summary-dashboard keys ===")
    print(list(data.keys()))
    kpis = data.get('kpis', {})
    print("KPIs keys (regions):", list(kpis.keys()))
    print("KPIs['overall'] contents:")
    for k, v in kpis.get('overall', {}).items():
        print(f"  {k}: {v}")
else:
    print("Error:", res.text)

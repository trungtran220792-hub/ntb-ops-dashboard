import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_url = 'http://127.0.0.1:5000'
auth = ('admin', 'admin123')

url = f"{base_url}/api/operational"
res = requests.get(url, auth=auth)
if res.status_code == 200:
    data = res.json()
    print("=== /api/operational response ===")
    for k, v in data.items():
        if isinstance(v, list):
            print(f"{k}: list of size {len(v)}: {v[:2]}")
        else:
            print(f"{k}: {v}")
else:
    print("Error:", res.text)

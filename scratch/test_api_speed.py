import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import time

base_url = 'http://127.0.0.1:5000'
auth = ('admin', 'admin123')

date_param = "2026-06-09+-+Th\u1ee9+3"

endpoints = [
    f"/api/summary-dashboard?date={date_param}&time_group=ngay",
    f"/api/trends-dashboard?date={date_param}&time_group=ngay",
    f"/api/matrix-tables?date={date_param}&time_group=ngay",
    "/api/operational",
    "/api/opr",
    "/api/backlog",
    "/api/volume-creation"
]

for ep in endpoints:
    url = f"{base_url}{ep}"
    print(f"Querying {ep}...")
    start = time.time()
    res = requests.get(url, auth=auth)
    elapsed = time.time() - start
    print(f"  Status code: {res.status_code}")
    print(f"  Response time: {elapsed:.4f}s")
    if res.status_code == 200:
        data = res.json()
        print(f"  Keys: {list(data.keys())[:5]}")
    else:
        print(f"  Error: {res.text[:100]}")
    print("-" * 40)

import requests
import json

url = "http://127.0.0.1:5000/api/sync/status"
auth = ('admin', 'admin123')

try:
    r = requests.get(url, auth=auth, timeout=10)
    r.raise_for_status()
    with open('sync_status.txt', 'w', encoding='utf-8') as f:
        json.dump(r.json(), f, indent=4, ensure_ascii=False)
    print("Done!")
except Exception as e:
    with open('sync_status.txt', 'w', encoding='utf-8') as f:
        f.write(f"Error: {e}")
    print("Error:", e)

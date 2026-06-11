import requests
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

sync_url = "http://127.0.0.1:5000/api/sync"
status_url = "http://127.0.0.1:5000/api/sync/status"

headers = {
    "Authorization": "Basic YWRtaW46YWRtaW4xMjM="
}

try:
    print("Triggering sync...")
    res = requests.post(sync_url, headers=headers, json={}, timeout=10)
    print("Trigger Status code:", res.status_code)
    print("Trigger Response:", res.json())
    
    if res.status_code == 200:
        print("Polling sync status...")
        for _ in range(30):
            time.sleep(1)
            status_res = requests.get(status_url, headers=headers, timeout=5)
            status_data = status_res.json()
            print(f"Status: {status_data.get('status')}, Progress: {status_data.get('progress')}")
            if status_data.get('status') in ['success', 'error']:
                print("Final Status:", status_data)
                break
    else:
        print("Failed to trigger sync.")
except Exception as e:
    print("Error:", e)

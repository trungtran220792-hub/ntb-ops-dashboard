import requests
import time

url = "https://dashboard-ntb.onrender.com/api/sync/status"
auth = ('admin', 'admin123')

print("Starting final poll...")
for i in range(20):
    try:
        res = requests.get(url, auth=auth, timeout=10)
        if res.status_code == 200:
            data = res.json()
            print(f"[{i*5}s] Status: {data.get('status')} | Progress: {data.get('progress')}")
            if data.get('status') == 'success':
                print("Completed successfully!")
                break
        else:
            print(f"Status code: {res.status_code}")
    except Exception as e:
        print(f"Failed: {e}")
    time.sleep(5)

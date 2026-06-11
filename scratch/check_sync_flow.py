import requests
import time

url_sync = "https://dashboard-ntb.onrender.com/api/sync"
url_status = "https://dashboard-ntb.onrender.com/api/sync/status"
auth = ('admin', 'admin123')

print("Waiting 90 seconds for Render to deploy the new code...")
time.sleep(90)

# 1. Trigger Sync
print("Triggering sync...")
try:
    res = requests.post(url_sync, auth=auth, timeout=30)
    print(f"Trigger Sync response: {res.status_code} - {res.text}")
except Exception as e:
    print(f"Failed to trigger sync: {e}")
    sys.exit(1)

# 2. Poll Status
start_time = time.time()
print("Polling sync status (max 5 minutes)...")
while time.time() - start_time < 300:
    try:
        res = requests.get(url_status, auth=auth, timeout=10)
        if res.status_code == 200:
            data = res.json()
            status = data.get("status")
            progress = data.get("progress")
            error = data.get("error")
            print(f"[{time.time() - start_time:.1f}s] Status: {status} | Progress: {progress} | Error: {error}")
            
            if status == "success":
                print("Sync completed successfully!")
                break
            elif status == "error":
                print(f"Sync failed with error: {error}")
                break
        else:
            print(f"[{time.time() - start_time:.1f}s] Non-200 status code: {res.status_code}")
    except Exception as e:
        print(f"[{time.time() - start_time:.1f}s] Poll request failed: {e}")
        
    time.sleep(5)

import requests

url = "http://127.0.0.1:5000/api/sync/status"
auth = ('admin', 'admin123')

try:
    print("Fetching sync status...")
    r = requests.get(url, auth=auth, timeout=10)
    r.raise_for_status()
    print("Response:", r.json())
except Exception as e:
    print("Error:", e)

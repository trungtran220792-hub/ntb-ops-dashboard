# -*- coding: utf-8 -*-
import requests
import json
import sys

def check_status():
    sys.stdout.reconfigure(encoding='utf-8')
    BASE_URL = "http://127.0.0.1:5000"
    session = requests.Session()
    
    # Login
    session.post(f"{BASE_URL}/api/login", json={"username": "admin", "password": "admin123"})
    
    res = session.get(f"{BASE_URL}/api/sync/status")
    print("Sync status code:", res.status_code)
    if res.status_code == 200:
        print("Sync status JSON:", json.dumps(res.json(), indent=4, ensure_ascii=False))
    else:
        print("Error content:", res.text)

if __name__ == "__main__":
    check_status()

# -*- coding: utf-8 -*-
import requests
import json
import sys

def check_dashboard():
    sys.stdout.reconfigure(encoding='utf-8')
    BASE_URL = "http://127.0.0.1:5000"
    session = requests.Session()
    
    # Login
    session.post(f"{BASE_URL}/api/login", json={"username": "admin", "password": "admin123"})
    
    res = session.get(f"{BASE_URL}/api/summary-dashboard")
    print("Summary dashboard status code:", res.status_code)
    if res.status_code == 200:
        data = res.json()
        print("Keys in summary dashboard data:", list(data.keys()))
        print("Date:", data.get("date"))
        print("Today's stats:", data.get("today"))
    else:
        print("Error content:", res.text)

if __name__ == "__main__":
    check_dashboard()

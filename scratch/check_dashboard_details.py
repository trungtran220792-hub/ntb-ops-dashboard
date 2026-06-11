# -*- coding: utf-8 -*-
import requests
import json
import sys

def check_dashboard_details():
    sys.stdout.reconfigure(encoding='utf-8')
    BASE_URL = "http://127.0.0.1:5000"
    session = requests.Session()
    session.post(f"{BASE_URL}/api/login", json={"username": "admin", "password": "admin123"})
    
    res = session.get(f"{BASE_URL}/api/summary-dashboard")
    if res.status_code == 200:
        data = res.json()
        print("latest_date:", data.get("latest_date"))
        overall = data.get("kpis", {}).get("overall", {})
        with open("scratch/overall_kpis.json", "w", encoding="utf-8") as f:
            json.dump(overall, f, indent=4, ensure_ascii=False)
        print("Saved to overall_kpis.json")
    else:
        print("Error content:", res.text)

if __name__ == "__main__":
    check_dashboard_details()

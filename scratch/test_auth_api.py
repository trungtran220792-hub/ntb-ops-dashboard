import requests
import json

session = requests.Session()
login_res = session.post("http://127.0.0.1:5000/api/login", json={
    "username": "admin",
    "password": "admin123"
})
print("Login status:", login_res.status_code)
print("Login body:", login_res.json())

if login_res.status_code == 200:
    res = session.get("http://127.0.0.1:5000/api/summary-dashboard")
    print("API status:", res.status_code)
    try:
        data = res.json()
        print("API keys in response:", data.keys() if isinstance(data, dict) else "Not a dict")
        if "overall" in data:
            print("Overall data:", data["overall"])
        else:
            print("Response:", str(data)[:300])
    except Exception as e:
        print("Failed to parse JSON:", e)
        print("Response text:", res.text[:300])

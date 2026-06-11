import requests

session = requests.Session()
login_res = session.post("http://127.0.0.1:5000/api/login", json={
    "username": "admin",
    "password": "admin123"
})
print("Login status:", login_res.status_code)

if login_res.status_code == 200:
    # Trigger warning endpoint
    res = session.post("http://127.0.0.1:5000/api/send-telegram-warning", json={})
    print("Warning response status:", res.status_code)
    print("Warning response body:", res.json())

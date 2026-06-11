import requests

session = requests.Session()
login_res = session.post("http://127.0.0.1:5000/api/login", json={
    "username": "admin",
    "password": "admin123"
})
print("Login status:", login_res.status_code)

if login_res.status_code == 200:
    res = session.post("http://127.0.0.1:5000/api/send-telegram-warning", json={})
    print("Warning response status:", res.status_code)
    try:
        # Save response safely as utf-8 file to read it
        with open("scratch/warning_error.json", "w", encoding="utf-8") as f:
            f.write(res.text)
        print("Error details saved to scratch/warning_error.json")
    except Exception as e:
        print("Failed to save response:", e)

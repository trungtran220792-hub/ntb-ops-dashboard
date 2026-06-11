import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_url = 'http://127.0.0.1:5000'
auth = ('admin', 'admin123')

# We need to authenticate and send a post request to /api/chat
url = f"{base_url}/api/chat"
payload = {"message": "odr tts"}
res = requests.post(url, json=payload, auth=auth)
if res.status_code == 200:
    print("Chatbot reply for 'odr tts':")
    print(res.json().get('reply'))
else:
    print("Error:", res.status_code, res.text)

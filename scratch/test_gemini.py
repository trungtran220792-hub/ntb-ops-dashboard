import os
import requests
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.environ.get("GEMINI_API_KEY", "").strip()

prompt = "Hãy viết một lời chào ngắn bằng tiếng Việt."
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_api_key}"
payload = {
    "contents": [{
        "parts": [{"text": prompt}]
    }]
}

try:
    res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
    print("Status Code:", res.status_code)
    print("Response:", res.text)
except Exception as e:
    print("Exception:", e)

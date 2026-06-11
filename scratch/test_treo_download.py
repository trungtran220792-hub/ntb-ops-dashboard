import requests

url = "https://docs.google.com/spreadsheets/d/1MjLW8NbD5ZjoOdd90myGv0i1NGAtlvScxebfAXMM1j8/export?format=xlsx"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
}

try:
    print("Sending GET request...")
    # stream=True to check headers first
    response = requests.get(url, headers=headers, stream=True, timeout=60)
    print(f"Status Code: {response.status_code}")
    print("Headers:")
    for k, v in response.headers.items():
        print(f"  {k}: {v}")
        
    print("Reading content in chunks...")
    size = 0
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            size += len(chunk)
            print(f"Read {size} bytes...", end="\r")
    print(f"\nFinished reading. Total size: {size} bytes")
except Exception as e:
    print(f"\nError occurred: {str(e)}")

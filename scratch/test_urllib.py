import urllib.request
import time

url = "https://docs.google.com/spreadsheets/d/1MjLW8NbD5ZjoOdd90myGv0i1NGAtlvScxebfAXMM1j8/export?format=xlsx"
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
)

start = time.time()
try:
    print("Downloading using urllib.request...")
    with urllib.request.urlopen(req, timeout=60) as response:
        content = response.read()
        print(f"Success! Read {len(content)} bytes in {time.time() - start:.2f} seconds.")
        with open("test_urllib.xlsx", "wb") as f:
            f.write(content)
except Exception as e:
    print(f"Failed in {time.time() - start:.2f} seconds: {str(e)}")

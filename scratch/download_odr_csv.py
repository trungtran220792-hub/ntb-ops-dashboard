import urllib.request
import os

url = "https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/export?format=csv&gid=1884142015"
output_path = "ODR TTS.csv"

try:
    print("Downloading ODR TTS.csv...")
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        content = response.read()
        with open(output_path, 'wb') as f:
            f.write(content)
    print("Download completed successfully! Size:", os.path.getsize(output_path), "bytes")
except Exception as e:
    print("Error:", e)

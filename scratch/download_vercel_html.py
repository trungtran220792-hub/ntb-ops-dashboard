import urllib.request
import ssl

url = "https://baocaovanhanhntb-tivk.vercel.app/"
output = r"scratch/vercel_index.html"

# Bypass SSL verification if needed
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    print(f"Downloading {url}...")
    with urllib.request.urlopen(url, context=ctx) as response:
        html = response.read()
    with open(output, "wb") as f:
        f.write(html)
    print(f"Success! Saved to {output} (Size: {len(html)} bytes)")
except Exception as e:
    print("Error downloading Vercel page:", e)

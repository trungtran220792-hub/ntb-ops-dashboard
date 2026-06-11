import urllib.request
import ssl

url = "http://127.0.0.1:5000/"
output = r"c:\Users\lap4all\Desktop\New folder\scratch\local_html_fetched.html"

# Bypass SSL verification if needed
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    print(f"Downloading from local server {url}...")
    # Add a User-Agent or host header if needed
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req, context=ctx) as response:
        html = response.read()
    with open(output, "wb") as f:
        f.write(html)
    print(f"Success! Saved to {output} (Size: {len(html)} bytes)")
    
    # Check if switchNtbRegion and renderOprDashboard exist
    html_str = html.decode('utf-8', errors='ignore')
    print("switchNtbRegion count:", html_str.count("switchNtbRegion"))
    print("renderOprDashboard count:", html_str.count("renderOprDashboard"))
    
except Exception as e:
    print("Error fetching from local server:", e)

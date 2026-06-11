import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://dashboard-ntb.onrender.com/"
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0')
try:
    print("Fetching Render site with 90s timeout...")
    with urllib.request.urlopen(req, timeout=90) as res:
        html = res.read().decode('utf-8')
    print("Fetched Render HTML. Length:", len(html))
    
    # Check if customized elements exist
    print("Has kpi-gan:", "kpi-gan" in html)
    print("Has kpi-gan-tts:", "kpi-gan-tts" in html)
    print("Has kpi-odr:", "kpi-odr" in html)
    print("Has Giới thiệu NTB:", "Giới thiệu NTB" in html)
    
    # Save it to a file
    with open("scratch/render_index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Saved to scratch/render_index.html")
except Exception as e:
    print("Error fetching Render site:", e)

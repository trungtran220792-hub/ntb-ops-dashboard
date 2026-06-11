import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import download_google_sheet

# Test downloading treo_url using the real app.py function
treo_url = "https://docs.google.com/spreadsheets/d/1MjLW8NbD5ZjoOdd90myGv0i1NGAtlvScxebfAXMM1j8/edit?gid=2146039156#gid=2146039156"
filepath = "test_app_treo.xlsx"

print("Testing download_google_sheet from app.py...")
success, msg = download_google_sheet(treo_url, filepath)
print(f"Status: {success}")

if success and os.path.exists(filepath):
    print(f"File downloaded successfully! Size: {os.path.getsize(filepath)} bytes")
    # Clean up test file
    try:
        os.remove(filepath)
    except:
        pass
else:
    print("Download failed!")

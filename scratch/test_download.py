import re
import requests
import sys

def download_google_sheet(url, output_path):
    if not url or not url.strip():
        return True, "No link, using local file."
        
    url = url.strip()
    if not (url.startswith("https://docs.google.com/spreadsheets/") or url.startswith("http://docs.google.com/spreadsheets/")):
        return False, "Invalid link. Must start with https://docs.google.com/spreadsheets/"
        
    match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
    if not match:
        return False, "No valid Spreadsheet ID found."
        
    spreadsheet_id = match.group(1)
    export_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=xlsx"
    
    print(f"Export URL: {export_url}")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        }
        response = requests.get(export_url, headers=headers, timeout=60)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True, "Download success."
        else:
            return False, f"Download failed (Status code: {response.status_code}). Please check sharing settings."
    except Exception as e:
        return False, f"Connection error: {str(e)}"

# Test the URLs
urls = {
    "ops": "https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/edit?gid=1365110988#gid=1365110988",
    "opr": "https://docs.google.com/spreadsheets/d/1B-QCbEnPpILFFEWPYheGdmkgYV9gSf4lAyQMlhzwOCM/edit?gid=124347012#gid=124347012",
    "aging": "https://docs.google.com/spreadsheets/d/1WCzgao34cA_SttyB9ytHfE1qKTNl_3iFqDbEfw3lbyU/edit?gid=1040733966#gid=1040733966",
    "treo": "https://docs.google.com/spreadsheets/d/1MjLW8NbD5ZjoOdd90myGv0i1NGAtlvScxebfAXMM1j8/edit?gid=2146039156#gid=2146039156",
}

for name, url in urls.items():
    print(f"Downloading {name}...")
    success, msg = download_google_sheet(url, f"test_{name}.xlsx")
    print(f"{name} status: {success}, msg: {msg}")

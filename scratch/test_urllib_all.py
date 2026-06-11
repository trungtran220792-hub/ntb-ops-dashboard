import re
import urllib.request
import time

def download_google_sheet_urllib(url, output_path):
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
    
    req = urllib.request.Request(
        export_url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            content = response.read()
            with open(output_path, "wb") as f:
                f.write(content)
            return True, f"Success ({len(content)} bytes)."
    except Exception as e:
        return False, f"Error: {str(e)}"

urls = {
    "ops_url": "https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/edit?gid=1365110988#gid=1365110988",
    "opr_url": "https://docs.google.com/spreadsheets/d/1B-QCbEnPpILFFEWPYheGdmkgYV9gSf4lAyQMlhzwOCM/edit?gid=124347012#gid=124347012",
    "aging_url": "https://docs.google.com/spreadsheets/d/1WCzgao34cA_SttyB9ytHfE1qKTNl_3iFqDbEfw3lbyU/edit?gid=1040733966#gid=1040733966",
    "treo_url": "https://docs.google.com/spreadsheets/d/1MjLW8NbD5ZjoOdd90myGv0i1NGAtlvScxebfAXMM1j8/edit?gid=2146039156#gid=2146039156",
    "bat_on_url": "https://docs.google.com/spreadsheets/d/1lmQv8KwHJzDFs_RMz64ydu4SOmG3M1YAzILNFGtzFec/edit?gid=250113221#gid=250113221",
    "off_spe_url": "https://docs.google.com/spreadsheets/d/1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg/edit?gid=1524249564#gid=1524249564",
    "tao_don_url": "https://docs.google.com/spreadsheets/d/1OygEPTn6Qu8okwAqpbx_RBiYQr1cfpO5hiaxqu4AMNE/edit?gid=872540531#gid=872540531"
}

for name, url in urls.items():
    print(f"Downloading {name}...")
    start = time.time()
    success, msg = download_google_sheet_urllib(url, f"test_{name}.xlsx")
    print(f"{name} status: {success}, msg: {msg} in {time.time() - start:.2f} seconds")

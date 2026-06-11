import urllib.request
import re
import sys
import os
import json
from dotenv import load_dotenv

load_dotenv()

config = {
    "ops_url": os.environ.get("OPS_URL", ""),
    "opr_url": os.environ.get("OPR_URL", ""),
    "aging_url": os.environ.get("AGING_URL", ""),
    "treo_url": os.environ.get("TREO_URL", ""),
    "bat_on_url": os.environ.get("BAT_ON_URL", ""),
    "off_spe_url": os.environ.get("OFF_SPE_URL", ""),
    "tao_don_url": os.environ.get("TAO_DON_URL", "")
}

mappings = [
    ("ops_url", 'Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', "Bao cao Van hanh"),
    ("opr_url", 'OPR TTS.xlsx', "OPR TTS"),
    ("aging_url", 'Aging _5 ngày.xlsx', "Aging 5 ngay"),
    ("treo_url", 'Treo luân chuyển GIAO_TRẢ by IMTHIR.xlsx', "Treo luan chuyen"),
    ("bat_on_url", 'buu_cuc_bat_on.xlsx', "Buu cuc bat on"),
    ("off_spe_url", 'off_tuyen_spe.xlsx', "OFF tuyen SPE"),
    ("tao_don_url", 'vols_tao_don.xlsx', "Volume tao don")
]

def download_sheet(url, output_path):
    # Print clean ascii filename and url
    clean_out = output_path.encode('ascii', 'ignore').decode('ascii')
    print(f"Downloading to {clean_out}")
    match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
    if not match:
        print("Invalid URL")
        return False
    spreadsheet_id = match.group(1)
    export_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=xlsx"
    try:
        req = urllib.request.Request(
            export_url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=60) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        print("Success")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

for key, filename, label in mappings:
    url = config.get(key, "")
    if url:
        download_sheet(url, filename)
    else:
        print(f"No URL for {label}")

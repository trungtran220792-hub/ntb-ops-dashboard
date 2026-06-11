import urllib.request
import re
import pandas as pd
import json

# Load config
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

ops_url = config.get('ops_url')

match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', ops_url)
spreadsheet_id = match.group(1)
export_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=xlsx"

output_path = 'scratch/downloaded_ops.xlsx'

# Reuse download if already present to make it fast
import os
if not os.path.exists(output_path):
    print("Downloading spreadsheet...")
    req = urllib.request.Request(
        export_url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        content = response.read()
        with open(output_path, 'wb') as f:
            f.write(content)
else:
    print("Using cached downloaded file...")

# Inspect downloaded sheet
with pd.ExcelFile(output_path) as xls:
    df_cc = None
    for s in xls.sheet_names:
        if 'cơ cấu' in s.lower() or 'co cau' in s.lower():
            df_cc = pd.read_excel(xls, sheet_name=s)
            break
            
    results = []
    results.append(f"Sheets: {xls.sheet_names}")
    if df_cc is not None:
        results.append(f"Columns: {list(df_cc.columns)}")
        targets = [
            'Điểm Xử Lý Hàng Thôn 2-Xã Nhân Cơ-Đắk Nông',
            'Điểm Xử Lý Hàng TDP 8 Quốc Lộ 14-Đông Gia Nghĩa-Lâm Đồng',
            'Điểm lấy hàng Nguyễn Đình Chiểu-Nghĩa Tân-Gia Nghĩa-Đăk Nông'
        ]
        for t in targets:
            match_row = df_cc[df_cc['Bưu cục'].astype(str).str.strip().str.lower() == t.strip().lower()]
            results.append(f"\nTarget '{t}': matches={len(match_row)}")
            if len(match_row) > 0:
                results.append(match_row.to_string())
    else:
        results.append("Cơ cấu sheet not found!")

with open('scratch/online_ops_inspect.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))
print("Done!")

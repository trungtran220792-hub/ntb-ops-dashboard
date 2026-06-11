import pandas as pd
import os

files = {
    'Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx': 'Cơ cấu',
    'Aging _5 ngày.xlsx': 'Cơ cấu',
    'Treo luân chuyển GIAO_TRẢ by IMTHIR.xlsx': 'Cơ cấu'
}

targets = [
    'điểm xử lý hàng thôn 2-xã nhân cơ-đắk nông',
    'điểm xử lý hàng tdp 8 quốc lộ 14-đông gia nghĩa-lâm đồng',
    'điểm lấy hàng nguyễn đình chiểu-nghĩa tân-gia nghĩa-đăk nông'
]

output = []

for filename, sheetname in files.items():
    if not os.path.exists(filename):
        output.append(f"File {filename} does not exist!")
        continue
    output.append(f"\n=== File: {filename} (Sheet: {sheetname}) ===")
    with pd.ExcelFile(filename) as xls:
        df = pd.read_excel(xls, sheet_name=sheetname)
        output.append(f"Columns: {list(df.columns)}")
        
        bc_col = next((c for c in df.columns if c.lower() == 'bc'), None)
        name_col = next((c for c in df.columns if 'bưu cục' in c.lower() or 'buu cuc' in c.lower()), None)
        
        matches = pd.DataFrame()
        if bc_col:
            matches_bc = df[df[bc_col].astype(str).str.strip().str.lower().isin(targets)]
            matches = pd.concat([matches, matches_bc])
        if name_col:
            matches_name = df[df[name_col].astype(str).str.strip().str.lower().isin(targets)]
            matches = pd.concat([matches, matches_name])
            
        matches = matches.drop_duplicates()
        output.append(f"Matches found: {len(matches)}")
        if len(matches) > 0:
            output.append(matches.to_string())

with open('scratch/all_cocau_inspect.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
print("Done!")

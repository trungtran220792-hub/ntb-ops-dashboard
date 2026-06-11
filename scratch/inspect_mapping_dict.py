import pandas as pd

def clean_str(val):
    if pd.isna(val):
        return ""
    return str(val).strip().lower()

def read_ops_sheet(xls, sheet_type):
    sheet_names_lower = [s.strip().lower() for s in xls.sheet_names]
    if sheet_type == "co_cau":
        for candidate in ["cơ cấu", "co cau"]:
            if candidate in sheet_names_lower:
                idx = sheet_names_lower.index(candidate)
                return pd.read_excel(xls, sheet_name=xls.sheet_names[idx])
        raise ValueError(f"Không tìm thấy sheet Cơ cấu. Sheets: {xls.sheet_names}")

file_path = 'Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx'
bc_to_am = {}
bc_to_prov = {}

with pd.ExcelFile(file_path) as xls:
    df_co_cau = read_ops_sheet(xls, "co_cau")

output = []
output.append(f"df_co_cau columns: {list(df_co_cau.columns)}")

for idx, r in df_co_cau.iterrows():
    bc = str(r.get('BC', '')).strip().lower()
    buucuc = str(r.get('Bưu cục', '')).strip().lower()
    
    am = ""
    for col in ['Am', 'AM', 'am', 'ID - Họ Tên Am', 'ID - Họ Tên AM']:
        if col in r:
            val = str(r.get(col, '')).strip()
            if val and val.lower() != 'nan':
                am = val
                break
    
    prov = ""
    for col in ['Tỉnh', 'TINH', 'tỉnh', 'tinh', 'Province', 'province']:
        if col in r:
            val = str(r.get(col, '')).strip()
            if val and val.lower() != 'nan':
                prov = val
                break
                
    if prov == 'Bình Phước':
        prov = 'Lâm Đồng'
        
    targets_to_inspect = [
        'điểm xử lý hàng thôn 2-xã nhân cơ-đắk nông',
        'điểm xử lý hàng tdp 8 quốc lộ 14-đông gia nghĩa-lâm đồng',
        'điểm lấy hàng nguyễn đình chiểu-nghĩa tân-gia nghĩa-đăk nông'
    ]
    if bc in targets_to_inspect or buucuc in targets_to_inspect:
        output.append(f"Row {idx}: bc='{bc}', buucuc='{buucuc}', am='{am}', prov='{prov}'")
        
    if bc and bc != 'nan':
        if am:
            bc_to_am[bc] = am
        if prov:
            bc_to_prov[bc] = prov
    if buucuc and buucuc != 'nan':
        if am:
            bc_to_am[buucuc] = am
        if prov:
            bc_to_prov[buucuc] = prov

output.append("\n--- bc_to_am query ---")
for t in targets_to_inspect:
    output.append(f"'{t}': am='{bc_to_am.get(t)}', prov='{bc_to_prov.get(t)}'")

with open('scratch/mapping_dict_inspect.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
print("Done!")

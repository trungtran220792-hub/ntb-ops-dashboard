import pandas as pd

xls = pd.ExcelFile('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx')
df_co_cau = pd.read_excel(xls, 'Cơ cấu')
df_ltc = pd.read_excel(xls, 'DataLTC')

bc_to_am = {}
for _, r in df_co_cau.iterrows():
    bc = str(r.get('BC', '')).strip().lower()
    buucuc = str(r.get('Bưu cục', '')).strip().lower()
    am = str(r.get('Am', r.get('ID - Họ Tên Am', ''))).strip()
    if bc and bc != 'nan':
        bc_to_am[bc] = am
    if buucuc and buucuc != 'nan':
        bc_to_am[buucuc] = am

targets = [
    'Điểm Xử Lý Hàng Thôn 2-Xã Nhân Cơ-Đắk Nông',
    'Điểm Xử Lý Hàng TDP 8 Quốc Lộ 14-Đông Gia Nghĩa-Lâm Đồng',
    'Điểm lấy hàng Nguyễn Đình Chiểu-Nghĩa Tân-Gia Nghĩa-Đăk Nông'
]

out = []
for t in targets:
    clean_t = t.strip().lower()
    mapped = bc_to_am.get(clean_t, 'NOT FOUND')
    out.append(f"Target: '{t}'")
    out.append(f"  clean_t: '{clean_t}'")
    out.append(f"  mapped: '{mapped}'")
    
    # Check if they are in bc_to_am keys
    in_keys = clean_t in bc_to_am
    out.append(f"  clean_t in bc_to_am: {in_keys}")
    
    # Print character by character hex values for clean_t and the key in bc_to_am
    if in_keys:
        key_in_dict = clean_t
    else:
        # Find closest key
        matches = [k for k in bc_to_am.keys() if 'tdp 8' in k or 'nhân cơ' in k or 'chiểu' in k]
        key_in_dict = matches[0] if matches else None
        
    out.append(f"  key_in_dict: '{key_in_dict}'")
    if key_in_dict:
        out.append(f"  clean_t hex: {[hex(ord(c)) for c in clean_t]}")
        out.append(f"  key_in_dict hex: {[hex(ord(c)) for c in key_in_dict]}")
        out.append(f"  Equal? {clean_t == key_in_dict}")

with open('debug_chars.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print("Completed!")

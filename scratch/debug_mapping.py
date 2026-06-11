import pandas as pd
import os

xls = pd.ExcelFile('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx')
df_co_cau = pd.read_excel(xls, 'Cơ cấu')
df_ltc = pd.read_excel(xls, 'DataLTC')
bc_to_am = {}
bc_to_prov = {}

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
    
    # Check similar keys
    similar = [k for k in bc_to_am.keys() if 'tdp' in k or 'nhân cơ' in k or 'chiểu' in k or 'thôn 2' in k]
    out.append(f"  Similar keys in bc_to_am: {similar}")
    
    # Check if they exist in df_ltc and what their clean_bc is
    matching_ltc = df_ltc[df_ltc['Chi tiết'].str.contains('tdp 8|thôn 2|chiểu', case=False, na=False)]['Chi tiết'].unique()
    out.append(f"  Matching in df_ltc: {list(matching_ltc)}")

with open('debug_mapping.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print("Debug file written successfully!")

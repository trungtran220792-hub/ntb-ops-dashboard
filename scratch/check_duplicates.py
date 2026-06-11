import pandas as pd

xls = pd.ExcelFile('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx')
df_co_cau = pd.read_excel(xls, 'Cơ cấu')

targets = [
    'Điểm Xử Lý Hàng Thôn 2-Xã Nhân Cơ-Đắk Nông',
    'Điểm Xử Lý Hàng TDP 8 Quốc Lộ 14-Đông Gia Nghĩa-Lâm Đồng',
    'Điểm lấy hàng Nguyễn Đình Chiểu-Nghĩa Tân-Gia Nghĩa-Đăk Nông'
]

out = []
for t in targets:
    out.append(f"=== Target: '{t}' ===")
    matches_bc = df_co_cau[df_co_cau['BC'].astype(str).str.strip().str.lower() == t.strip().lower()]
    matches_buucuc = df_co_cau[df_co_cau['Bưu cục'].astype(str).str.strip().str.lower() == t.strip().lower()]
    
    out.append(f"Matches in BC column: {len(matches_bc)}")
    for idx, r in matches_bc.iterrows():
        out.append(f"  Row {idx}: {dict(r)}")
        
    out.append(f"Matches in Bưu cục column: {len(matches_buucuc)}")
    for idx, r in matches_buucuc.iterrows():
        out.append(f"  Row {idx}: {dict(r)}")

with open('debug_duplicates.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print("Done!")

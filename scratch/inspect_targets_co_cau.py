import pandas as pd

targets = [
    'Điểm Xử Lý Hàng Thôn 2-Xã Nhân Cơ-Đắk Nông',
    'Điểm Xử Lý Hàng TDP 8 Quốc Lộ 14-Đông Gia Nghĩa-Lâm Đồng',
    'Điểm lấy hàng Nguyễn Đình Chiểu-Nghĩa Tân-Gia Nghĩa-Đăk Nông'
]

output = []

# 1. Inspect in Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx
file_path = 'Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx'
with pd.ExcelFile(file_path) as xls:
    df_cc = pd.read_excel(xls, sheet_name='Cơ cấu')
    output.append("=== Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx (Cơ cấu sheet) ===")
    for t in targets:
        # Check by Bưu cục or BC column
        match1 = df_cc[df_cc['Bưu cục'].astype(str).str.strip().str.lower() == t.strip().lower()]
        match2 = df_cc[df_cc['BC'].astype(str).str.strip().str.lower() == t.strip().lower()]
        output.append(f"Target '{t}':")
        output.append(f"  Matches by 'Bưu cục': {len(match1)}")
        if len(match1) > 0:
            output.append(match1.to_string())
        output.append(f"  Matches by 'BC': {len(match2)}")
        if len(match2) > 0:
            output.append(match2.to_string())

# 2. Inspect in co_cau_ntb.xlsx
file_path_ntb = 'co_cau_ntb.xlsx'
df_ntb = pd.read_excel(file_path_ntb)
output.append("\n=== co_cau_ntb.xlsx ===")
for t in targets:
    match = df_ntb[df_ntb['Bưu cục'].astype(str).str.strip().str.lower() == t.strip().lower()]
    output.append(f"Target '{t}':")
    output.append(f"  Matches: {len(match)}")
    if len(match) > 0:
        output.append(match.to_string())

with open('scratch/targets_co_cau_inspect.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
print("Done!")

import pandas as pd
from app import get_dataframes

df_gtc, df_ltc, df_aging, df_treo = get_dataframes(force=True)

targets = [
    'Điểm Xử Lý Hàng Thôn 2-Xã Nhân Cơ-Đắk Nông',
    'Điểm Xử Lý Hàng TDP 8 Quốc Lộ 14-Đông Gia Nghĩa-Lâm Đồng',
    'Điểm lấy hàng Nguyễn Đình Chiểu-Nghĩa Tân-Gia Nghĩa-Đăk Nông'
]

output = []
output.append("=== Verification of df_gtc mapping ===")
for t in targets:
    matches_gtc = df_gtc[df_gtc['Chi tiết'] == t]
    output.append(f"\nTarget in df_gtc: '{t}'")
    output.append(f"  Matches: {len(matches_gtc)}")
    for idx, r in matches_gtc.iterrows():
        r_dict = {
            'Chi tiết': r.get('Chi tiết'),
            'clean_bc': r.get('clean_bc'),
            'mapped_am': r.get('mapped_am'),
            'mapped_prov': r.get('mapped_prov'),
            'AM': r.get('AM')
        }
        output.append(f"    Row {idx}: {r_dict}")

with open('scratch/gtc_targets_inspect.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
print("Done!")

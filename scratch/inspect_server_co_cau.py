import pandas as pd
from app import get_dataframes

print("Calling get_dataframes(force=True)...")
df_gtc, df_ltc, df_aging, df_treo = get_dataframes(force=True)

targets = [
    'Điểm Xử Lý Hàng Thôn 2-Xã Nhân Cơ-Đắk Nông',
    'Điểm Xử Lý Hàng TDP 8 Quốc Lộ 14-Đông Gia Nghĩa-Lâm Đồng',
    'Điểm lấy hàng Nguyễn Đình Chiểu-Nghĩa Tân-Gia Nghĩa-Đăk Nông'
]

out = []
out.append("=== Verification of get_dataframes() Caching ===")
out.append(f"df_ltc columns: {list(df_ltc.columns)}")

for t in targets:
    out.append(f"\nTarget: '{t}'")
    # Search in df_ltc
    matches_ltc = df_ltc[df_ltc['Chi tiết'] == t]
    out.append(f"  Matches in df_ltc: {len(matches_ltc)}")
    for idx, r in matches_ltc.iterrows():
        # print specific columns of interest
        cols_of_interest = ['Chi tiết', 'clean_bc', 'mapped_am', 'mapped_prov']
        # check if other am columns exist
        other_am_cols = [c for c in df_ltc.columns if 'am' in c.lower()]
        for c in other_am_cols:
            if c not in cols_of_interest:
                cols_of_interest.append(c)
        r_dict = {c: r[c] for c in cols_of_interest if c in df_ltc.columns}
        out.append(f"    Row {idx}: {r_dict}")

with open('debug_server_co_cau.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print("Completed!")

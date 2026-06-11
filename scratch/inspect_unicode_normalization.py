import pandas as pd
import unicodedata

def inspect_string(s):
    if not isinstance(s, str):
        return str(s)
    chars = []
    for c in s:
        name = unicodedata.name(c, 'UNKNOWN')
        chars.append(f"{c} ({hex(ord(c))} - {name})")
    return "\n  ".join(chars)

file_path = 'Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx'

with pd.ExcelFile(file_path) as xls:
    df_cc = pd.read_excel(xls, sheet_name='Cơ cấu')
    df_ltc = pd.read_excel(xls, sheet_name='DataLTC')

# Targets in df_cc
targets_cc = df_cc[df_cc['Bưu cục'].astype(str).str.contains('Thôn 2-Xã Nhân Cơ', case=False)]
# Targets in df_ltc
targets_ltc = df_ltc[df_ltc['Chi tiết'].astype(str).str.contains('Thôn 2-Xã Nhân Cơ', case=False)]

output = []
output.append("=== Inspecting 'Điểm Xử Lý Hàng Thôn 2-Xã Nhân Cơ-Đắk Nông' ===")
if not targets_cc.empty:
    val_cc = targets_cc.iloc[0]['Bưu cục']
    output.append(f"In 'Cơ cấu' sheet (value = '{val_cc}'):")
    output.append(inspect_string(val_cc))
else:
    output.append("Not found in 'Cơ cấu' sheet")

if not targets_ltc.empty:
    val_ltc = targets_ltc.iloc[0]['Chi tiết']
    output.append(f"\nIn 'DataLTC' sheet (value = '{val_ltc}'):")
    output.append(inspect_string(val_ltc))
else:
    output.append("Not found in 'DataLTC' sheet")

# Compare clean versions
if not targets_cc.empty and not targets_ltc.empty:
    clean_cc = val_cc.strip().lower()
    clean_ltc = val_ltc.strip().lower()
    output.append(f"\nClean equal? {clean_cc == clean_ltc}")
    output.append(f"Clean CC bytes: {clean_cc.encode('utf-8')}")
    output.append(f"Clean LTC bytes: {clean_ltc.encode('utf-8')}")

with open('scratch/unicode_inspect.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
print("Done!")

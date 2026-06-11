import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

xls_path = "scratch/temp_download.xlsx"
df = pd.read_excel(xls_path, sheet_name="Nhân Sự")

# Apply filters:
# Trạng thái == "Đang làm việc"
# Vùng == "NTB"
# Chức vụ == "Business Development Field Executive"
# SP Team? == False
cond = (
    (df['Trạng thái'] == "Đang làm việc") & 
    (df['Vùng'] == "NTB") & 
    (df['Chức vụ'] == "Business Development Field Executive") & 
    (df['SP Team?'] == False)
)
filtered = df[cond]

print("Filtered headcount size:", len(filtered))
print("Unique PO count:", len(filtered['Bưu cục'].unique()))

print("\nCounts by PO:")
po_counts = filtered.groupby('Bưu cục').size().reset_index(name='hc')

names = ["56 Phan", "40A Yết Kiêu", "466 Đường 23/10", "115 Lý Nam Đế", "575 Đường 8/4", "309 Đường 8/4"]
for name in names:
    matched = po_counts[po_counts['Bưu cục'].str.contains(name, na=False)]
    for _, r in matched.iterrows():
        print(f"  {r['Bưu cục']}: hc={r['hc']}")

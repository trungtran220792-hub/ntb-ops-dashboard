import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

xls_path = "scratch/temp_download.xlsx"
df = pd.read_excel(xls_path, sheet_name="Nhân Sự")

# Filter active NTB employees
active_ntb = df[(df['Trạng thái'] == "Đang làm việc") & (df['Vùng'] == "NTB")]

# Filter by Chức vụ == 'Business Development Field Executive'
bdf = active_ntb[active_ntb['Chức vụ'] == 'Business Development Field Executive']

print("Total BDF count:", len(bdf))
print("Unique POs count:", len(bdf['Bưu cục'].unique()))

print("\nCounts by PO for BDF (top 15):")
po_counts = bdf.groupby('Bưu cục').size().reset_index(name='hc')
print(po_counts.sort_values(by='hc', ascending=False).head(15))

# Check for specific names
names = ["56 Phan", "40A Yết Kiêu", "466 Đường 23/10", "115 Lý Nam Đế", "575 Đường 8/4", "309 Đường 8/4"]
print("\nMatching counts for BDF:")
for name in names:
    matched = po_counts[po_counts['Bưu cục'].str.contains(name, na=False)]
    for _, r in matched.iterrows():
        print(f"  {r['Bưu cục']}: hc={r['hc']}")

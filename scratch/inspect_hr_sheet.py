import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

xls_path = "scratch/temp_download.xlsx"
df_ns = pd.read_excel(xls_path, sheet_name="Nhân Sự")

print("Columns in Nhân Sự:", df_ns.columns)
print("Unique values of Trạng thái:", df_ns['Trạng thái'].unique())
print("Unique values of Vùng:", df_ns['Vùng'].unique())

# Filter active NTB employees
active_ntb = df_ns[(df_ns['Trạng thái'] == "Đang làm việc") & (df_ns['Vùng'] == "NTB")]
print("\nTotal active NTB employees:", len(active_ntb))

# List top 15 post offices in active NTB by employee count
po_counts = active_ntb.groupby('Bưu cục').size().reset_index(name='headcount')
print("\nTop 15 Bưu cục by active headcount:")
print(po_counts.sort_values(by='headcount', ascending=False).head(15))

# Let's inspect Bưu cục names that contain "Phan Đình Phùng", "Yết Kiêu", "Đường 23/10", "Lý Nam Đế", "Đường 8/4"
names = ["Phan Đình Phùng", "Yết Kiêu", "Đường 23/10", "Lý Nam Đế", "Đường 8/4"]
print("\nMatching active POs:")
for name in names:
    matched = po_counts[po_counts['Bưu cục'].str.contains(name, na=False)]
    for _, r in matched.iterrows():
        print(f"  {r['Bưu cục']}: headcount={r['headcount']}")
        
# Let's see if we group by the exact string of Bưu cục after parsing
# Usually they are of format "warehouse_id - Bưu cục name"
# Let's parse warehouse_id and name
def parse_po(po_str):
    if pd.isna(po_str):
        return None, None
    parts = str(po_str).split(" - ", 1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return None, str(po_str).strip()

active_ntb['parsed_id'], active_ntb['parsed_name'] = zip(*active_ntb['Bưu cục'].map(parse_po))
print("\nUnique parsed PO names and their active headcount (top 15):")
parsed_counts = active_ntb.groupby('parsed_name').size().reset_index(name='headcount')
print(parsed_counts.sort_values(by='headcount', ascending=False).head(15))

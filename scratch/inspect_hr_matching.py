import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

xls_path = "scratch/temp_download.xlsx"
df_ns = pd.read_excel(xls_path, sheet_name="Nhân Sự")
df_data = pd.read_excel(xls_path, sheet_name="Data")
df_cc = pd.read_excel(xls_path, sheet_name="CoCauVung")

print("Checking Nhân Sự for active NTB:")
active_ns = df_ns[df_ns['Trạng thái'] == "Đang làm việc"]
active_ns_ntb = active_ns[active_ns['Vùng'] == "NTB"]
print("Total active in NTB:", len(active_ns_ntb))
print("Unique post offices in active NTB:", len(active_ns_ntb['Bưu cục'].unique()))

# Let's see if 762 active in NTB matches!
# Let's group by Bưu cục
print("\nUnique post offices in active NTB counts:")
print(active_ns_ntb.groupby('Bưu cục').size().sort_values(ascending=False).head(10))

# Let's find "Bưu Cục 56 Phan Đình Phùng" in df_ns
# We saw Bưu Cục 56 Phan Đình Phùng has 13 in the screenshot.
# Let's search for "56 Phan" in df_ns['Bưu cục']
matched_po = [po for po in active_ns_ntb['Bưu cục'].unique() if "56 Phan" in str(po)]
print("\nMatched POs for 56 Phan in active NTB:")
for po in matched_po:
    count = len(active_ns_ntb[active_ns_ntb['Bưu cục'] == po])
    print(f"  {po}: {count}")

# Let's see how volumes are calculated!
# In the screenshot:
# Grand Total Volume TB/Ngày = 44,209
# Let's calculate total average volume from Data sheet
dates = df_data['Time'].unique()
print(f"\nUnique dates in Data sheet: {len(dates)}")
total_vol_by_date = df_data.groupby('Time')['Volume'].sum()
print("Average total daily volume in Data sheet:", total_vol_by_date.mean())

# Let's see if we group by Chi tiết in df_data and sum/len(dates)
po_avg_vol = df_data.groupby('Chi tiết')['Volume'].sum() / len(dates)
print("\nSum of PO average volumes:", po_avg_vol.sum())

# Let's match Bưu cục names between Nhân Sự and Data
# In df_ns, Bưu cục is e.g. "22830000 - Bưu Cục 56 Phan Đình Phùng-Cam Linh-Khánh Hòa"
# In df_data, Chi tiết is e.g. "BC 56 Phan Đình Phùng-Cam Linh-Khánh Hòa" or "Bưu Cục 56 Phan Đình Phùng-Cam Linh-Khánh Hòa"?
# Let's search df_data['Chi tiết'] for "56 Phan"
matched_data_po = [po for po in df_data['Chi tiết'].unique() if "56 Phan" in str(po)]
print("\nMatched POs in df_data for 56 Phan:")
for po in matched_data_po:
    print(f"  {po}: avg vol = {po_avg_vol[po]}")

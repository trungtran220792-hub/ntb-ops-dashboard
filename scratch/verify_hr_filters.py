import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

xls_path = "scratch/temp_download.xlsx"
df = pd.read_excel(xls_path, sheet_name="Nhân Sự")

active_ntb = df[(df['Trạng thái'] == 'Đang làm việc') & (df['Vùng'] == 'NTB')]
print("Active NTB Total:", len(active_ntb))

# Let's filter by Chức vụ
print("\nFilter by Chức vụ == 'Business Development Field Executive':")
bdf = active_ntb[active_ntb['Chức vụ'] == 'Business Development Field Executive']
print("Count:", len(bdf))
print("Unique POs count:", len(bdf['Bưu cục'].unique()))

# Filter by other Chức vụ to see what they are
print("\nFilter by other Chức vụ:")
print(active_ntb['Chức vụ'].value_counts())

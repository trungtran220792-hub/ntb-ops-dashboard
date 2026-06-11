import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

xls_path = "scratch/temp_download.xlsx"
df = pd.read_excel(xls_path, sheet_name="Nhân Sự")

print("Original size:", len(df))

# Let's try different filters
# Possible columns: 'Chức vụ', 'Trạng thái', 'Loại HĐ', 'Vùng', 'SP Team?'
print("\nUnique values in SP Team?:", df['SP Team?'].unique())
print("Unique values in Loại HĐ:", df['Loại HĐ'].unique())
print("Unique values in Chức vụ:", df['Chức vụ'].unique())

# Try filtering by SP Team? == False
print("\nFiltering by SP Team? == False:")
df_f1 = df[df['SP Team?'] == False]
print("  Active NTB size:", len(df_f1[(df_f1['Trạng thái'] == 'Đang làm việc') & (df_f1['Vùng'] == 'NTB')]))
print("  Unique POs:", len(df_f1[(df_f1['Trạng thái'] == 'Đang làm việc') & (df_f1['Vùng'] == 'NTB')]['Bưu cục'].unique()))

# Try filtering by SP Team? == True
print("\nFiltering by SP Team? == True:")
df_f2 = df[df['SP Team?'] == True]
print("  Active NTB size:", len(df_f2[(df_f2['Trạng thái'] == 'Đang làm việc') & (df_f2['Vùng'] == 'NTB')]))
print("  Unique POs:", len(df_f2[(df_f2['Trạng thái'] == 'Đang làm việc') & (df_f2['Vùng'] == 'NTB')]['Bưu cục'].unique()))

# Try filtering out certain Chức vụ (e.g. Business Development Field Executive or Delivery or whatever?)
print("\nChức vụ value counts:")
print(df['Chức vụ'].value_counts())

# Let's try combining:
# If we check Vùng == 'NTB' and see which rows are active
active_ntb = df[(df['Trạng thái'] == 'Đang làm việc') & (df['Vùng'] == 'NTB')]
print("\nactive_ntb SP Team? counts:")
print(active_ntb['SP Team?'].value_counts())
print("\nactive_ntb Loại HĐ counts:")
print(active_ntb['Loại HĐ'].value_counts())

# What if we exclude 'HĐDV' (Hợp đồng dịch vụ) or 'HĐLĐ'?
# Wait, let's look at the counts of unique Bưu cục for active_ntb
print("Unique PO count in active_ntb:", len(active_ntb['Bưu cục'].unique()))

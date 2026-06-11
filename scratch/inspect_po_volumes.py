import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

xls_path = "scratch/temp_download.xlsx"
df_data = pd.read_excel(xls_path, sheet_name="Data")

# Let's search for "Phan Đình Phùng" in Data sheet
pdf_data = df_data[df_data['Chi tiết'].str.contains("Phan Đình Phùng", na=False)]
print("Unique Chi tiết for 'Phan Đình Phùng' in Data:")
print(pdf_data['Chi tiết'].unique())

print("\nUnique Time in Data for 'Phan Đình Phùng':")
print(pdf_data['Time'].unique())

print("\nGroup by Chi tiết and Time volume sum:")
daily_vols = pdf_data.groupby(['Chi tiết', 'Time'])['Volume'].sum().reset_index()
print(daily_vols.head(20))

print("\nMean of daily volumes for each 'Phan Đình Phùng' post office:")
print(daily_vols.groupby('Chi tiết')['Volume'].mean())

print("\nLet's print the sum of Volume for each 'Phan Đình Phùng' post office:")
print(pdf_data.groupby('Chi tiết')['Volume'].sum())

# Let's print unique 'Loại Hàng' for them
print("\nUnique 'Loại Hàng' for 'Phan Đình Phùng' POs:")
print(pdf_data.groupby(['Chi tiết', 'Loại Hàng'])['Volume'].sum())

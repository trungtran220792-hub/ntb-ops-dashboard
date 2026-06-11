import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

xls_path = "scratch/temp_download.xlsx"
df = pd.read_excel(xls_path, sheet_name="shopee_tiktok")

print("Columns in shopee_tiktok:", df.columns)
print("\nUnique dates in shopee_tiktok:")
print(df['Date'].unique())
print("Total rows:", len(df))

# Let's search for "Phan Đình Phùng" in Bưu cục column
pdf = df[df['Bưu cục'].str.contains("Phan Đình Phùng", na=False)]
print("\nUnique Bưu cục for 'Phan Đình Phùng':")
print(pdf['Bưu cục'].unique())

print("\nGroup by Bưu cục and sum of Volume:")
print(pdf.groupby('Bưu cục')['Volume'].sum())

# Let's print unique dates in pdf
print("\nUnique dates for 'Phan Đình Phùng' in shopee_tiktok:")
print(pdf['Date'].unique())

# Let's print daily volumes for 'Phan Đình Phùng' POs
print("\nDaily volumes for 'Phan Đình Phùng' POs:")
print(pdf.groupby(['Bưu cục', 'Date'])['Volume'].sum().reset_index())

import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Loading data...")
xls_path = "scratch/temp_download.xlsx"
df_data = pd.read_excel(xls_path, sheet_name="Data")
df_ns = pd.read_excel(xls_path, sheet_name="Nhân Sự")

print("Data columns:", df_data.columns)
print("Nhân Sự columns:", df_ns.columns)

# Calculate average daily volume for each post office in Data sheet
# Wait, let's check unique dates in Data sheet
dates = df_data['Time'].unique()
print(f"Number of unique dates in Data sheet: {len(dates)}")
print("Sample dates:", list(dates[:5]))

# Group by Chi tiết to get sum of Volume divided by number of unique dates?
# Or is it the average of Volume for each Chi tiết?
# Let's calculate the sum of Volume for each Chi tiết, divided by unique dates.
num_dates = len(dates)
po_vol = df_data.groupby('Chi tiết')['Volume'].sum() / num_dates
print("\nTop 10 volumes by average daily volume in Data sheet:")
print(po_vol.sort_values(ascending=False).head(10))

# Let's count active headcounts by post office from df_ns
# Trạng thái == "Đang làm việc"
active_ns = df_ns[df_ns['Trạng thái'] == "Đang làm việc"]
print(f"\nTotal active employees: {len(active_ns)}")
print("Unique post offices in df_ns:", len(active_ns['Bưu cục'].unique()))

ns_counts = active_ns.groupby('Bưu cục').size()
print("\nTop 10 post offices by employee count:")
print(ns_counts.sort_values(ascending=False).head(10))

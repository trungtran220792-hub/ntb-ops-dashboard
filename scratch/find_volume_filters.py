import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

xls_path = "scratch/temp_download.xlsx"
df_data = pd.read_excel(xls_path, sheet_name="Data")
print("Loại Hàng values:", df_data['Loại Hàng'].unique())

dates = df_data['Time'].unique()
num_dates = len(dates)

# Let's try grouping by Chi tiết and Jenis (Loại Hàng) and see average volumes
for lh in df_data['Loại Hàng'].unique():
    df_filtered = df_data[df_data['Loại Hàng'] == lh]
    po_avg = df_filtered.groupby('Chi tiết')['Volume'].sum() / num_dates
    print(f"\n--- Filter: Loại Hàng = {lh} ---")
    targets = ["56 Phan", "115 Lý Nam Đế", "575 Đường 8/4", "40A Yết Kiêu", "466 Đường 23/10", "309 Đường 8/4"]
    for name in targets:
        matches = [po for po in po_avg.index if name.lower() in str(po).lower()]
        for po in matches:
            print(f"  {po}: {po_avg[po]:.2f}")
            
# Let's also check if the average volume is calculated as the mean of the daily volumes (since some POs might not have data for all days, so mean of daily volumes is different from sum / total_days)
print("\n--- Average computed as Po Daily mean ---")
# Group by Chi tiết and Time to get daily sum of Volume
po_daily = df_data.groupby(['Chi tiết', 'Time'])['Volume'].sum().reset_index()
po_mean = po_daily.groupby('Chi tiết')['Volume'].mean()
targets = ["56 Phan", "115 Lý Nam Đế", "575 Đường 8/4", "40A Yết Kiêu", "466 Đường 23/10", "309 Đường 8/4"]
for name in targets:
    matches = [po for po in po_mean.index if name.lower() in str(po).lower()]
    for po in matches:
        print(f"  {po}: {po_mean[po]:.2f}")

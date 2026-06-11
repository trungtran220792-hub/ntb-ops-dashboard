import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

xls_path = "scratch/temp_download.xlsx"
df = pd.read_excel(xls_path, sheet_name="Data")

print("Columns in Data:", df.columns)
print("Unique dates count in Data:", len(df['Time'].unique()))

names = ["Phan Đình Phùng", "Lý Nam Để", "Đường 8/4", "Yết Kiêu", "Đường 23/10"]
for name in names:
    pdf = df[df['Chi tiết'].str.contains(name, na=False)]
    print(f"\nMatches for '{name}' in Data:")
    for po in pdf['Chi tiết'].unique():
        po_df = pdf[pdf['Chi tiết'] == po]
        total_vol = po_df['Volume'].sum()
        # Group by date to get daily volume sum, then take the average
        daily_sums = po_df.groupby('Time')['Volume'].sum()
        avg_vol = daily_sums.mean()
        print(f"  {po}: sum={total_vol}, unique_dates_with_data={len(daily_sums)}, average_vol={avg_vol:.2f}")

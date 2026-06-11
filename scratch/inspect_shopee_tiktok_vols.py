import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

xls_path = "scratch/temp_download.xlsx"
df = pd.read_excel(xls_path, sheet_name="shopee_tiktok")

# Filter by Vùng == 'NTB'
df_ntb = df[df['Vùng'] == 'NTB']
print("Total rows in NTB shopee_tiktok:", len(df_ntb))

# Group by Bưu cục and calculate mean daily volume
# Number of unique dates in NTB shopee_tiktok
num_dates = len(df_ntb['Date'].unique())
print("Number of unique dates in NTB shopee_tiktok:", num_dates)

po_sums = df_ntb.groupby('Bưu cục')['Volume'].sum()
po_avgs = po_sums / num_dates

print("\nDaily Averages (sum / num_dates) for top 15 POs in NTB shopee_tiktok:")
print(po_avgs.sort_values(ascending=False).head(15))

# Check for "Phan Đình Phùng"
pdf = df_ntb[df_ntb['Bưu cục'].str.contains("Phan Đình Phùng", na=False)]
print("\nPhan Đình Phùng POs in NTB shopee_tiktok:")
for po in pdf['Bưu cục'].unique():
    sum_vol = pdf[pdf['Bưu cục'] == po]['Volume'].sum()
    avg_vol = sum_vol / num_dates
    print(f"  {po}: sum={sum_vol}, avg={avg_vol:.2f}")

# Group by warehouse_id
po_ids = df_ntb.groupby('warehouse_id')['Volume'].sum() / num_dates
print("\nTop 15 warehouse_ids by average daily volume:")
print(po_ids.sort_values(ascending=False).head(15))

# Let's see if warehouse_id matches CoCauVung
df_cc = pd.read_excel(xls_path, sheet_name="CoCauVung")
# Join po_ids with CoCauVung
df_cc_merged = df_cc.merge(po_ids.reset_index(name='avg_daily_vol'), on='warehouse_id', how='left')
print("\nTop 15 from CoCauVung with shopee_tiktok volumes:")
print(df_cc_merged.sort_values(by='avg_daily_vol', ascending=False).head(15))

# Print specific post offices in CoCauVung
names = ["56 Phan", "Yết Kiêu", "Đường 23/10", "Lý Nam Đế", "Đường 8/4"]
print("\nTarget POs from CoCauVung:")
for name in names:
    matched = df_cc_merged[df_cc_merged['Bưu cục'].str.contains(name, na=False)]
    for _, r in matched.iterrows():
        print(f"  {r['warehouse_id']} - {r['Bưu cục']}: avg_daily_vol={r['avg_daily_vol']:.2f}")

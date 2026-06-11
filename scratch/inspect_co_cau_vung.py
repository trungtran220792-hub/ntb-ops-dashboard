import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

xls_path = "scratch/temp_download.xlsx"
df_cc = pd.read_excel(xls_path, sheet_name="CoCauVung")

print("CoCauVung total rows:", len(df_cc))
print("CoCauVung columns:", df_cc.columns)

# Write to a file
with open("scratch/co_cau_vung_dump.txt", "w", encoding="utf-8") as f:
    f.write("=== CoCauVung Dump ===\n")
    f.write(df_cc.to_string())

print("Dump complete.")

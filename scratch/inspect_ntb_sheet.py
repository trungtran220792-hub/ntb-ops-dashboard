import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

xls_path = "scratch/temp_download.xlsx"
df = pd.read_excel(xls_path, sheet_name="NTB")

print("NTB columns:", df.columns)
print("NTB shape:", df.shape)
print("\nFirst 10 rows of NTB:")
print(df.head(10))

# Search for target volume numbers in NTB sheet
targets = [1852, 957, 1098, 783, 1299, 1164, 608]
print("\nTarget number searches in NTB sheet:")
for col in df.columns:
    for idx, val in enumerate(df[col]):
        try:
            val_num = float(val)
            if any(abs(val_num - t) < 1.0 for t in targets):
                print(f"  FOUND {val} in column '{col}' at index {idx}")
        except:
            pass

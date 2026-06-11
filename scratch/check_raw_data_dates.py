import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
sys.path.append(workspace_dir)

from app import get_dataframes

df_gtc, df_ltc, df_aging, df_treo = get_dataframes(force=True)

print("df_gtc Time unique values:")
print(sorted(df_gtc['Time'].dropna().unique().tolist()))

print("\ndf_ltc Time unique values:")
print(sorted(df_ltc['Time'].dropna().unique().tolist()))

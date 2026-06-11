import sys
import os
sys.path.append(os.getcwd())
sys.stdout.reconfigure(encoding='utf-8')

from app import get_dataframes
df_gtc, df_ltc, df_aging, df_treo = get_dataframes(force=True)

print("Unique mapped_am in df_aging:")
print(df_aging['mapped_am'].value_counts(dropna=False))

print("\nUnique mapped_am in df_treo:")
print(df_treo['mapped_am'].value_counts(dropna=False))

print("\nUnique mapped_am in df_gtc:")
print(df_gtc['mapped_am'].value_counts(dropna=False))

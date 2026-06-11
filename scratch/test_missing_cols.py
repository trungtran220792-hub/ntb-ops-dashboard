import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Let's test if df_gtc['Tỉnh'] raises KeyError when 'Tỉnh' column is missing
df = pd.DataFrame({'clean_bc': ['bc1'], 'Volume': [10]})
bc_to_prov = {'bc1': 'Lâm Đồng'}

try:
    df['mapped_prov'] = df['clean_bc'].map(bc_to_prov).fillna(df['Tỉnh'])
except Exception as e:
    print("Error raised:", type(e), str(e))

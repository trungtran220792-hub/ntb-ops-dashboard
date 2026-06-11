import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
import os

for f in ['aging_raw.csv', 'treo_stuck.csv']:
    if os.path.exists(f):
        try:
            df = pd.read_csv(f, nrows=5)
            print(f"{f} columns:", list(df.columns))
        except Exception as e:
            print(f"Error reading {f}: {e}")
    else:
        print(f"{f} does not exist.")

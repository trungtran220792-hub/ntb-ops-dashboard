import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
import os

for f in ['opr_opr.csv', 'opr_oe.csv', 'opr_raw.csv']:
    if os.path.exists(f):
        try:
            df = pd.read_csv(f, nrows=10)
            print(f"\n{f} columns: {list(df.columns)}")
            print(df.head(5))
        except Exception as e:
            print(f"Error reading {f}: {e}")
    else:
        print(f"{f} does not exist.")

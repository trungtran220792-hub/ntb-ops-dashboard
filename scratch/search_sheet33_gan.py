import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    df = pd.read_excel('OPR TTS.xlsx', sheet_name='Sheet33')
    print("Columns:", list(df.columns))
    print("Unique dates:", df['Time'].unique())
    
    print("\n--- Sheet33 DAILY OVERALL % GÁN ---")
    for date, group in df.groupby('Time'):
        vol = group['Volume'].sum()
        # % Gán might be pre-calculated in the rows, we can calculate a weighted average
        # if % Gán exists, does Sản Lượng Gán exist?
        # Let's check if there is a column for Sản Lượng Gán, or calculate it.
        # Wait, does the sheet have Product of Volume * % Gán?
        # Let's print the first few rows to see if % Gán is string/float
        pass
        
    print(df.iloc[:20].to_string())
except Exception as e:
    print("Error:", e)

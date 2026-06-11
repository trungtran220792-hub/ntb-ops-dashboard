import sys
import os

# Set up path to import app
sys.path.append("c:/Users/lap4all/Desktop/New folder")

try:
    import pandas as pd
    import numpy as np
    
    # Try importing elements from app.py to run the function logic
    # Or let's just inspect app.py's load_volume_creation logic
    print("Reading vols_tao_don.csv...")
    if os.path.exists("vols_tao_don.csv"):
        df = pd.read_csv("vols_tao_don.csv")
        print("vols_tao_don.csv read successfully! Shape:", df.shape)
        print("Columns:", list(df.columns))
    else:
        print("vols_tao_don.csv does not exist!")

    if os.path.exists("vols_tao_don.xlsx"):
        print("vols_tao_don.xlsx exists! Reading first few rows...")
        df_xl = pd.read_excel("vols_tao_don.xlsx", nrows=5)
        print("Columns in Excel:", list(df_xl.columns))

except Exception as e:
    print("Error during test:", e)
    import traceback
    traceback.print_exc()

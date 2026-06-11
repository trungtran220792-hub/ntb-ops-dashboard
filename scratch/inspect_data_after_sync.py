import os
import datetime
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = 'ODR TTS.csv'
if os.path.exists(filepath):
    mtime = os.path.getmtime(filepath)
    mtime_dt = datetime.datetime.fromtimestamp(mtime)
    print(f"File: {filepath}")
    print(f"Last Modified: {mtime_dt}")
    print(f"File Size: {os.path.getsize(filepath)} bytes")
    df = pd.read_csv(filepath)
    print("Columns:", df.columns.tolist())
    print("Shape:", df.shape)
    print("Time values:")
    print(df['Time'].value_counts())
else:
    print(f"File {filepath} does not exist.")

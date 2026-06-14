import os
import sys
sys.path.insert(0, os.getcwd())

import pandas as pd
from app import load_df_from_db, resolve_path, get_db_engine

def compare():
    engine = get_db_engine()
    if engine is None:
        print("No DB engine initialized.")
        return

    files = [
        'ops_gtc.csv',
        'ops_ltc.csv',
        'opr_opr.csv',
        'opr_oe.csv',
        'aging_raw.csv',
        'treo_stuck.csv',
        'buu_cuc_bat_on.csv',
        'vols_tao_don.csv',
        'ops_nhan_su.csv',
        'ops_co_cau.csv'
    ]
    
    for f in files:
        csv_path = resolve_path(f, write=False)
        print(f"\n--- Checking file: {f} ---")
        if os.path.exists(csv_path):
            csv_mtime = os.path.getmtime(csv_path)
            import datetime
            csv_time = datetime.datetime.fromtimestamp(csv_mtime).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Local CSV exists. Modified time: {csv_time}, Size: {os.path.getsize(csv_path)} bytes")
            try:
                csv_df = pd.read_csv(csv_path)
                print(f"Local CSV shape: {csv_df.shape}")
                # Print unique dates if column 'Time' or 'Date' exists
                for col in ['Time', 'Date', 'NgayLTC']:
                    if col in csv_df.columns:
                        print(f"  Local CSV {col} unique values: {csv_df[col].dropna().unique()[-5:]}")
            except Exception as e:
                print(f"Error reading CSV: {e}")
        else:
            print("Local CSV does not exist.")

        # DB
        db_df = load_df_from_db(f)
        if db_df is not None:
            print(f"DB Table shape: {db_df.shape}")
            for col in ['Time', 'Date', 'NgayLTC']:
                if col in db_df.columns:
                    print(f"  DB Table {col} unique values: {db_df[col].dropna().unique()[-5:]}")
        else:
            print("DB Table does not exist or cannot be loaded.")

if __name__ == '__main__':
    compare()

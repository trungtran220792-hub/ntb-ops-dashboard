import sys
import pandas as pd
import os

sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")

if os.path.exists(file_path):
    df = pd.read_excel(file_path, sheet_name="DataLTC")
    # For each date, compute total volume, total assigned volume, and weighted %Gán
    # Note that in DataLTC, column is '%Gán' (no space)
    df['assigned_vol'] = df['Volume'] * df['%Gán']
    grouped = df.groupby('Time').agg({'Volume': 'sum', 'assigned_vol': 'sum'}).reset_index()
    grouped['% Gán (weighted)'] = grouped['assigned_vol'] / grouped['Volume'] * 100
    
    print("=== LTC Sheet 'DataLTC' Daily Assign Rates (Weighted) ===")
    for idx, row in grouped.sort_values(by='Time', ascending=False).iterrows():
        print(f"Time: {row['Time']} | Volume: {row['Volume']} | % Gán: {row['% Gán (weighted)']:.4f}%")
        
    print("\n=== LTC Sheet 'DataLTC' Simple Average of %Gán ===")
    simple_grouped = df.groupby('Time')['%Gán'].mean() * 100
    for t, val in simple_grouped.sort_index(ascending=False).items():
        print(f"Time: {t} | Simple Avg % Gán: {val:.4f}%")
        
else:
    print("File not found")

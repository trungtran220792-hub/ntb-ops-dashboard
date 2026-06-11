import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")

with pd.ExcelFile(file_path) as xls:
    df_data = pd.read_excel(xls, "Data")
    print("Data sheet unique times:", df_data['Time'].dropna().unique().tolist())
    
    df_ltc = pd.read_excel(xls, "DataLTC")
    print("DataLTC sheet unique times:", df_ltc['Time'].dropna().unique().tolist())

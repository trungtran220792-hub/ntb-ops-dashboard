import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")

with pd.ExcelFile(file_path) as xls:
    df_ck = pd.read_excel(xls, "Thứ cùng kỳ")
    print("Columns:", list(df_ck.columns))
    print("Shape:", df_ck.shape)
    print("First 15 rows:\n", df_ck.head(15).to_string())

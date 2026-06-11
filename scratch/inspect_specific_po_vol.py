import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "inspect_specific_po_vol.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="DataLTC")
    df.columns = [c.strip() for c in df.columns]
    
    # 1. Print row 104
    f.write("=== Row 104 ===\n")
    f.write(str(df.iloc[104].to_dict()) + "\n\n")
    
    # 2. Print row 105
    f.write("=== Row 105 ===\n")
    f.write(str(df.iloc[105].to_dict()) + "\n\n")
    
    # 3. Print rows where '% LTC' is exactly or close to 0.9142
    f.write("=== Rows where '% LTC' is close to 0.9142 ===\n")
    # convert '% LTC' to numeric
    df['% LTC_num'] = pd.to_numeric(df['% LTC'], errors='coerce')
    matches = df[(df['% LTC_num'] >= 0.9141) & (df['% LTC_num'] <= 0.9143)]
    for idx, row in matches.iterrows():
        f.write(f"Index {idx}: {row.to_dict()}\n")

print("Done inspecting row.")

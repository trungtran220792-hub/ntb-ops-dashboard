import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
csv_path = os.path.join(workspace_dir, "thu_cung_ky.csv")
output_path = os.path.join(workspace_dir, "scratch", "check_thu_cung_ky_output.txt")

with open(output_path, "w", encoding="utf-8") as f:
    if not os.path.exists(csv_path):
        f.write("CSV not found\n")
        exit(1)
        
    df = pd.read_csv(csv_path)
    f.write(f"Columns: {list(df.columns)}\n")
    f.write(f"Shape: {df.shape}\n")
    f.write("First 20 rows:\n")
    f.write(df.head(20).to_string() + "\n")
    
    # Check if there is "Time" column
    if "Time" in df.columns:
        f.write(f"Unique times: {df['Time'].dropna().unique().tolist()}\n")
        
    # Check if there are other columns or sections
    # Often, CSVs from Google sheets can have multiple tables or sections.
    # Let's find rows containing text like "Tỉnh" or "AM"
    for col in df.columns:
        matching_rows = df[df[col].astype(str).str.contains("Tỉnh|AM|Bưu cục|Chi tiết", case=False, na=False)]
        if not matching_rows.empty:
            f.write(f"Found matching rows in column {col}:\n")
            f.write(matching_rows.head(10).to_string() + "\n")

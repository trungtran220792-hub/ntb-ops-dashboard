import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "find_looker_formula_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df_data = pd.read_excel(file_path, sheet_name="DataLTC")
    
    # 1. Search for value 0.9142 in any column
    f.write("=== Searching for 0.9142 in DataLTC ===\n")
    for col in df_data.columns:
        # Convert to numeric, handle string/percent formatting
        col_numeric = pd.to_numeric(df_data[col], errors='coerce')
        matches = df_data[(col_numeric >= 0.9141) & (col_numeric <= 0.9143)]
        if len(matches) > 0:
            f.write(f"Matches in column '{col}':\n")
            f.write(matches[[col]].head(10).to_string() + "\n\n")
            
    # 2. Let's calculate the average of '% LTC' column or weighted average
    f.write("=== Averages of % LTC column in DataLTC ===\n")
    df_data.columns = [c.strip() for c in df_data.columns]
    
    # Average of '% LTC'
    pct_ltc_col = pd.to_numeric(df_data['% LTC'], errors='coerce').dropna()
    f.write(f"Average of % LTC column: {pct_ltc_col.mean() * 100:.4f}%\n")
    
    # Weighted average: sum(Sản Lượng Lấy Thành Công) / sum(Volume)
    vol_col = pd.to_numeric(df_data['Volume'], errors='coerce').fillna(0)
    success_col = pd.to_numeric(df_data['Sản Lượng Lấy Thành Công'], errors='coerce').fillna(0)
    
    f.write(f"Total Volume in DataLTC: {vol_col.sum()}\n")
    f.write(f"Total success in DataLTC: {success_col.sum()}\n")
    f.write(f"Overall Success % (success / vol): {success_col.sum() / vol_col.sum() * 100:.4f}%\n")
    
    # Let's inspect unique values of Time
    f.write(f"Time column describe:\n")
    f.write(df_data['Time'].describe().to_string() + "\n")
    
    # Let's group by Time and calculate Success %
    f.write("=== Success % grouped by Time (first 20 rows) ===\n")
    grouped = df_data.groupby('Time').agg({
        'Volume': 'sum',
        'Sản Lượng Lấy Thành Công': 'sum'
    }).reset_index()
    grouped['% success'] = (grouped['Sản Lượng Lấy Thành Công'] / grouped['Volume']) * 100
    
    f.write(grouped.head(20).to_string() + "\n")
    
    # Let's search for any time group where % success is close to 91.42%
    f.write("\n=== Time groups with % success close to 91.42% ===\n")
    matches_group = grouped[(grouped['% success'] >= 91.41) & (grouped['% success'] <= 91.43)]
    f.write(matches_group.to_string() + "\n")
    
    # Let's search for any time group where average of % LTC is close to 91.42%
    grouped_avg_ltc = df_data.groupby('Time').agg({
        '% LTC': 'mean',
        'Volume': 'sum'
    }).reset_index()
    grouped_avg_ltc['% LTC_scaled'] = grouped_avg_ltc['% LTC'] * 100
    
    f.write("\n=== Time groups with avg % LTC close to 91.42% ===\n")
    matches_avg = grouped_avg_ltc[(grouped_avg_ltc['% LTC_scaled'] >= 91.41) & (grouped_avg_ltc['% LTC_scaled'] <= 91.43)]
    f.write(matches_avg.to_string() + "\n")

print("Done find_looker_formula.")

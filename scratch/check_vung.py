import pandas as pd

with open('scratch/check_vung_res.txt', 'a', encoding='utf-8') as f:
    f.write("\n=== CHECKING opr_opr.csv ===\n")
    try:
        df = pd.read_csv('opr_opr.csv')
        for col in df.columns:
            if 'vung' in col.lower() or 'tinh' in col.lower() or 'bc' in col.lower() or 'kho' in col.lower() or 'am' in col.lower():
                vals = df[col].dropna().unique()
                f.write(f"{col}: {list(vals[:20])}\n")
    except Exception as e:
        f.write(f"Error reading opr_opr.csv: {e}\n")
print("Done check_vung for OPR!")

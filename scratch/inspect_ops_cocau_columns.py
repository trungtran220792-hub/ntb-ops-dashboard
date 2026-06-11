import pandas as pd
file_path = 'Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx'
output = []
with pd.ExcelFile(file_path) as xls:
    output.append(f"Sheet names: {xls.sheet_names}")
    for s in xls.sheet_names:
        if 'cơ cấu' in s.lower() or 'co cau' in s.lower():
            df = pd.read_excel(xls, sheet_name=s)
            output.append(f"Columns for sheet '{s}': {list(df.columns)}")
            output.append("First 5 rows:")
            output.append(df.head(5).to_string())

with open('scratch/ops_cocau_inspect.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
print("Done!")

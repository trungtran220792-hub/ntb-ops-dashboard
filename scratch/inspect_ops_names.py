import pandas as pd

file_path = 'Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx'

targets_lower = [
    'điểm xử lý hàng thôn 2-xã nhân cơ-đắk nông',
    'điểm xử lý hàng tdp 8 quốc lộ 14-đông gia nghĩa-lâm đồng',
    'điểm lấy hàng nguyễn đình chiểu-nghĩa tân-gia nghĩa-đăk nông'
]

output = []

with pd.ExcelFile(file_path) as xls:
    # Check sheets
    for sheet in xls.sheet_names:
        if sheet.lower() in ['data', 'datagtc', 'rawltc', 'datalts', 'dataltc', 'ltc']:
            df = pd.read_excel(xls, sheet_name=sheet)
            output.append(f"\n=== Sheet '{sheet}' ===")
            output.append(f"Columns: {list(df.columns)}")
            
            # Find the column for 'Chi tiết' or similar
            det_col = next((c for c in df.columns if c.lower() == 'chi tiết' or c.lower() == 'chi tiet'), None)
            if det_col:
                # Find matching rows
                df['clean'] = df[det_col].astype(str).str.strip().str.lower()
                matches = df[df['clean'].isin(targets_lower)]
                output.append(f"Found {len(matches)} matching rows")
                if len(matches) > 0:
                    # Look for AM column
                    am_col = next((c for c in df.columns if 'am' in c.lower()), None)
                    show_cols = [det_col]
                    if am_col:
                        show_cols.append(am_col)
                    if 'Time' in df.columns:
                        show_cols.append('Time')
                    if 'Volume' in df.columns:
                        show_cols.append('Volume')
                    output.append(matches[show_cols].head(10).to_string())

with open('scratch/ops_names_inspect.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
print("Done!")

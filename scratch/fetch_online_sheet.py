import requests
import io
import pandas as pd

url = "https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/export?format=csv&gid=1666412390"

try:
    print("Fetching online sheet...")
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    
    df = pd.read_csv(io.StringIO(r.text))
    # Search for target rows
    targets = ['TDP 8', 'Thôn 2', 'Nguyễn Đình Chiểu']
    
    out = []
    out.append("=== Online Google Sheet 'Cơ cấu' Tab ===")
    out.append(f"Columns: {list(df.columns)}")
    
    # Check if 'Bưu cục' column exists
    bc_col = next((c for c in df.columns if 'bưu cục' in c.lower() or 'buu_cuc' in c.lower()), df.columns[1] if len(df.columns) > 1 else df.columns[0])
    
    matching = df[df[bc_col].astype(str).str.contains('TDP 8|Thôn 2|Nguyễn Đình Chiểu', case=False, na=False)]
    
    for idx, row in matching.iterrows():
        out.append(f"Row {idx}: {row.to_dict()}")
        
    with open('online_sheet_check.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    print("Done!")
    
except Exception as e:
    with open('online_sheet_check.txt', 'w', encoding='utf-8') as f:
        f.write(f"Error: {e}")
    print(f"Error: {e}")

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
import openpyxl
import os

xlsx_path = 'downloaded_consolidated_sheet.xlsx'
output_file = 'scratch/inspect_excel_sheets_res.txt'

with open(output_file, 'w', encoding='utf-8') as f_out:
    def log_print(*args):
        msg = " ".join(map(str, args))
        f_out.write(msg + "\n")

    try:
        if not os.path.exists(xlsx_path):
            log_print(f"Error: {xlsx_path} does not exist.")
        else:
            with pd.ExcelFile(xlsx_path) as xls:
                log_print("Sheet names:", xls.sheet_names)
                
                # Check matching for aging
                aging_sheets = [s for s in xls.sheet_names if any(c in s.strip().lower() for c in ["aging trên 5 ngày", "aging tren 5 ngay", "đơn giao aging trên 5 ngày", "don giao aging tren 5 ngay"])]
                log_print("Matched aging sheets:", aging_sheets)
                for s in aging_sheets:
                    df = pd.read_excel(xls, sheet_name=s, nrows=10)
                    log_print(f"\nSheet {s} columns: {list(df.columns)}")
                    log_print(f"Sheet {s} first 5 rows:")
                    log_print(df.head(5).to_string())
                    
                # Check matching for treo
                treo_sheets = [s for s in xls.sheet_names if any(c in s.strip().lower() for c in ["treo lc", "stuck", "treo luân chuyển", "treo luan chuyen"])]
                log_print("\nMatched treo sheets:", treo_sheets)
                for s in treo_sheets:
                    df = pd.read_excel(xls, sheet_name=s, nrows=10)
                    log_print(f"\nSheet {s} columns: {list(df.columns)}")
                    log_print(f"Sheet {s} first 5 rows:")
                    log_print(df.head(5).to_string())
                    
    except Exception as e:
        import traceback
        log_print("Error:", e)
        log_print(traceback.format_exc())

print("Inspection completed successfully.")

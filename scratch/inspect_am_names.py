import pandas as pd
import os
import sys
sys.path.append(r'c:\Users\lap4all\Desktop\New folder')
from app import resolve_path

out_file = r'c:\Users\lap4all\Desktop\New folder\scratch\am_names_output.txt'

with open(out_file, 'w', encoding='utf-8') as f_out:
    f_out.write("AM NAMES INSPECTION\n")
    f_out.write("===================\n\n")

def inspect_file(file_name, sheet_name, am_col):
    path = resolve_path(file_name, write=False)
    if not os.path.exists(path):
        with open(out_file, 'a', encoding='utf-8') as f_out:
            f_out.write(f"File {file_name} not found.\n")
        return
    try:
        df = pd.read_excel(path, sheet_name=sheet_name)
        if am_col in df.columns:
            unique_ams = df[am_col].dropna().unique()
            with open(out_file, 'a', encoding='utf-8') as f_out:
                f_out.write(f"\n{file_name} ({sheet_name}) unique AMs ({len(unique_ams)}):\n")
                for am in sorted(unique_ams):
                    f_out.write(f"  - {am}\n")
        else:
            with open(out_file, 'a', encoding='utf-8') as f_out:
                f_out.write(f"\nColumn {am_col} not found in {file_name} ({sheet_name}). Columns: {df.columns.tolist()[:5]}\n")
    except Exception as e:
        with open(out_file, 'a', encoding='utf-8') as f_out:
            f_out.write(f"Error reading {file_name}: {str(e)}\n")

# Inspect all files
inspect_file('OPR TTS.xlsx', 'OPR', 'AM')
inspect_file('Aging _5 ngày.xlsx', 'Cơ cấu', 'AM')
inspect_file('Treo luân chuyển GIAO_TRẢ by IMTHIR.xlsx', 'Cơ cấu', 'AM')
inspect_file('co_cau_ntb.xlsx', 'Sheet1', 'AM')

print("Done. Output written to scratch/am_names_output.txt")

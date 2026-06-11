import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.getcwd())

import pandas as pd

# Let's inspect map_po_to_am_prov dependencies
from app import load_sheet_cached, clean_po_name, map_po_to_am_prov, resolve_path

print("Loading co_cau_ntb...")
df_cc = pd.read_excel('co_cau_ntb.xlsx', sheet_name='Sheet1')

# Build mapping dicts
id_to_am = {}
id_to_prov = {}
name_to_am = {}
name_to_prov = {}

for _, r in df_cc.iterrows():
    bc_id = r.get('warehouse_id')
    bc_name = r.get('Bưu cục')
    am = r.get('AM')
    prov = r.get('Tỉnh')
    
    if pd.isna(bc_name):
        continue
    
    bc_name_str = str(bc_name).strip()
    am_str = str(am).strip() if pd.notna(am) else "Không xác định"
    prov_str = str(prov).strip() if pd.notna(prov) else "Không xác định"
    
    if prov_str == 'Khánh Hoà':
        prov_str = 'Khánh Hòa'
    if prov_str == 'Bình Phước':
        prov_str = 'Lâm Đồng'
        
    name_clean = clean_po_name(bc_name_str)
    name_to_am[name_clean] = am_str
    name_to_prov[name_clean] = prov_str
    
    if pd.notna(bc_id):
        try:
            pid = int(float(bc_id))
            id_to_am[pid] = am_str
            id_to_prov[pid] = prov_str
        except:
            pass

print(f"Mapped {len(name_to_am)} post office names.")

print("Loading ODR TTS.csv...")
df_odr = pd.read_csv('ODR TTS.csv')
print("Unique post offices in ODR TTS.csv:", len(df_odr['Chi tiết'].unique()))

matched_count = 0
unmatched_pos = set()

# Map each PO in ODR
for po_name in df_odr['Chi tiết'].dropna().unique():
    # Call map_po_to_am_prov (id = None since ODR CSV has no ID column)
    am_mapped, prov_mapped = map_po_to_am_prov(None, po_name, id_to_am, id_to_prov, name_to_am, name_to_prov)
    
    # Check if we got a valid mapping or default
    # If the clean province matches NTB - province, we can also use that as fallback
    if am_mapped != "Không xác định" or prov_mapped != "Không xác định":
        matched_count += 1
    else:
        unmatched_pos.add(po_name)

total_unique_pos = len(df_odr['Chi tiết'].dropna().unique())
print(f"Mapped {matched_count} out of {total_unique_pos} unique ODR post offices ({matched_count/total_unique_pos*100:.2f}%)")
print("Unmatched count:", len(unmatched_pos))
print("Unmatched sample:")
print(list(unmatched_pos)[:10])

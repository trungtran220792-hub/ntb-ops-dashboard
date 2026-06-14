import sys
import os
sys.path.append(os.getcwd())
sys.stdout.reconfigure(encoding='utf-8')

from app import api_nhan_su, app

with app.test_request_context():
    # Simulate GET request to /api/nhan-su
    # Bypass permission check by calling the view function directly if we can,
    # or just copy the logic inside api_nhan_su and run it.
    
    import pandas as pd
    import numpy as np
    from app import resolve_path, safe_read_csv
    
    try:
        ns_path = resolve_path('ops_nhan_su.csv', write=False)
        df_ns = safe_read_csv(ns_path)
        print("df_ns size:", len(df_ns) if df_ns is not None else "None")
        print("df_ns columns:", df_ns.columns.tolist() if df_ns is not None else "None")
        
        df_ns.columns = [c.strip() for c in df_ns.columns]
        
        def check_sp_team(x):
            val_str = str(x).strip().lower()
            return val_str in ['true', '1', 'yes', 't']
            
        active_mask = (
            (df_ns['Trạng thái'].astype(str).str.strip() == "Đang làm việc") &
            (df_ns['Vùng'].astype(str).str.strip() == "NTB") &
            (df_ns['Chức vụ'].astype(str).str.strip() == "Business Development Field Executive") &
            (~df_ns['SP Team?'].apply(check_sp_team))
        )
        active_df = df_ns[active_mask].copy()
        print("active_df size:", len(active_df))
        
        resigned_mask = (
            (df_ns['Trạng thái'].astype(str).str.strip() == "Đã nghỉ") &
            (df_ns['Vùng'].astype(str).str.strip() == "NTB")
        )
        resigned_count = len(df_ns[resigned_mask])
        print("resigned_count:", resigned_count)
        
        def parse_warehouse_id(bc_str):
            if pd.isna(bc_str):
                return None
            parts = str(bc_str).split(" - ", 1)
            if len(parts) == 2:
                try:
                    return int(parts[0].strip())
                except:
                    return parts[0].strip()
            return None
            
        active_df['warehouse_id'] = active_df['Bưu cục'].apply(parse_warehouse_id)
        print("active_df warehouse_ids unique count:", len(active_df['warehouse_id'].dropna().unique()))
        
        cc_path = resolve_path('ops_co_cau.csv', write=False)
        df_cc = safe_read_csv(cc_path)
        print("df_cc size:", len(df_cc) if df_cc is not None else "None")
        print("df_cc columns:", df_cc.columns.tolist() if df_cc is not None else "None")
        
        df_cc.columns = [c.strip() for c in df_cc.columns]
        
        def clean_id(x):
            try:
                return int(float(x))
            except:
                return str(x).strip()
                
        # Check if warehouse_id is in df_cc columns
        if 'warehouse_id' in df_cc.columns:
            df_cc['warehouse_id_clean'] = df_cc['warehouse_id'].apply(clean_id)
        else:
            print("WARNING: warehouse_id not in df_cc columns! Available:", df_cc.columns.tolist())
            # Let's see if there is another ID column, e.g. BC
            id_col = next((c for c in df_cc.columns if 'id' in c.lower() or 'bc' in c.lower()), None)
            if id_col:
                print("Fallback mapping from", id_col)
                df_cc['warehouse_id_clean'] = df_cc[id_col].apply(clean_id)
                
        active_df['warehouse_id_clean'] = active_df['warehouse_id'].apply(clean_id)
        
        # Check vols
        vol_path = resolve_path('vols_tao_don.csv', write=False)
        df_vol = safe_read_csv(vol_path)
        print("df_vol size:", len(df_vol) if df_vol is not None else "None")
        
    except Exception as e:
        print("Error executing diagnostic script:", e)
        import traceback
        traceback.print_exc()

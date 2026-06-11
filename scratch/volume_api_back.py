def get_volume_creation():
    global DF_TAO_DON_CACHE, DF_BUU_CUC_TYPE_MAP
    
    with CACHE_LOCK:
        if DF_TAO_DON_CACHE is None:
            DF_TAO_DON_CACHE = load_vols_tao_don_df()
        if DF_BUU_CUC_TYPE_MAP is None:
            DF_BUU_CUC_TYPE_MAP = load_buu_cuc_type_map()
            
    if DF_TAO_DON_CACHE is None:
        return jsonify({"error": "Không tìm thấy file vols_tao_don.xlsx. Vui lòng cấu hình Google Sheet và đồng bộ!"}), 404
        
    try:
        df = DF_TAO_DON_CACHE.copy()
        
        # Get query parameters
        province = request.args.get('province')
        district = request.args.get('district')
        ward = request.args.get('ward')
        post_office = request.args.get('post_office')
        customer = request.args.get('customer')
        po_type = request.args.get('po_type')
        date_range = request.args.get('date_range', '7d')
        
        # 1. Compute dynamic dropdown options based on cascaded filtering
        provinces_opt = sorted([str(x) for x in df['Tỉnh'].dropna().unique()])
        
        df_dist = df
        if province:
            df_dist = df_dist[df_dist['Tỉnh'] == province]
        districts_opt = sorted([str(x) for x in df_dist['Quận/Huyện'].dropna().unique()])
        
        df_ward = df_dist
        if district:
            df_ward = df_ward[df_ward['Quận/Huyện'] == district]
        wards_opt = sorted([str(x) for x in df_ward['Phường/Xã'].dropna().unique()])
        
        df_po = df_ward
        if ward:
            df_po = df_po[df_po['Phường/Xã'] == ward]
        post_offices_opt = sorted([str(x) for x in df_po['Bưu cục'].dropna().unique()])
        
        customers_opt = sorted([str(x) for x in df['Khách hàng'].dropna().unique()])
        po_types_opt = ['BC', 'GXT']
        
        # 2. Apply dropdown filters to our dataframe copies
        df_filtered = df.copy()
        if province:
            df_filtered = df_filtered[df_filtered['Tỉnh'] == province]
        if district:
            df_filtered = df_filtered[df_filtered['Quận/Huyện'] == district]
        if ward:
            df_filtered = df_filtered[df_filtered['Phường/Xã'] == ward]
        if post_office:
            df_filtered = df_filtered[df_filtered['Bưu cục'] == post_office]
        if customer:
            df_filtered = df_filtered[df_filtered['Khách hàng'] == customer]
        if po_type:
            if DF_BUU_CUC_TYPE_MAP:
                df_filtered['po_type_mapped'] = df_filtered['warehouse_id'].map(DF_BUU_CUC_TYPE_MAP).fillna('BC')
                df_filtered = df_filtered[df_filtered['po_type_mapped'] == po_type]
            else:
                # Fallback if map not loaded
                pass
                
        latest_dt = df_filtered['Date'].max()
        if pd.isna(latest_dt):
            return jsonify({"error": "Không tìm thấy dữ liệu ngày hợp lệ sau khi lọc."}), 400
            
        # WTD & comparison calculations based on filtered dataset (before date range filter)
        weekday = latest_dt.weekday()
        wtd_start = latest_dt - pd.Timedelta(days=weekday)
        wtd_end = latest_dt
        
        wtd1_start = wtd_start - pd.Timedelta(days=7)
        wtd1_end = latest_dt - pd.Timedelta(days=7)
        
        wtd2_start = wtd_start - pd.Timedelta(days=14)
        wtd2_end = latest_dt - pd.Timedelta(days=14)
        
        def sum_range(df_sub, start, end):
            mask = (df_sub['Date'] >= start) & (df_sub['Date'] <= end)
            return df_sub[mask].groupby('Tỉnh')['Volume'].sum()
            
        wtd_sums = sum_range(df_filtered, wtd_start, wtd_end)
        wtd1_sums = sum_range(df_filtered, wtd1_start, wtd1_end)
        wtd2_sums = sum_range(df_filtered, wtd2_start, wtd2_end)
        
        d_dt = latest_dt
        d1_dt = latest_dt - pd.Timedelta(days=1)
        d2_dt = latest_dt - pd.Timedelta(days=2)
        d7_dt = latest_dt - pd.Timedelta(days=7)
        
        def sum_day(df_sub, dt):
            return df_sub[df_sub['Date'] == dt].groupby('Tỉnh')['Volume'].sum()
            
        d_sums = sum_day(df_filtered, d_dt)
        d1_sums = sum_day(df_filtered, d1_dt)
        d2_sums = sum_day(df_filtered, d2_dt)
        d7_sums = sum_day(df_filtered, d7_dt)
        
        provinces_list = ['Bình Thuận', 'Khánh Hòa', 'Lâm Đồng', 'Ninh Thuận', 'Đắk Nông']
        pivot_rows = []
        
        for p in provinces_list:
            wtd = float(wtd_sums.get(p, 0))
            wtd1 = float(wtd1_sums.get(p, 0))
            wtd2 = float(wtd2_sums.get(p, 0))
            
            d_val = float(d_sums.get(p, 0))
            d1_val = float(d1_sums.get(p, 0))
            d2_val = float(d2_sums.get(p, 0))
            d7_val = float(d7_sums.get(p, 0))
            
            wtd_wtd2 = ((wtd - wtd2) / wtd2 * 100) if wtd2 > 0 else 0.0
            wtd_wtd1 = ((wtd - wtd1) / wtd1 * 100) if wtd1 > 0 else 0.0
            d_d7 = ((d_val - d7_val) / d7_val * 100) if d7_val > 0 else 0.0
            d_d1 = ((d_val - d1_val) / d1_val * 100) if d1_val > 0 else 0.0
            
            pivot_rows.append({
                'province': p,
                'wtd2': int(wtd2),
                'wtd1': int(wtd1),
                'wtd': int(wtd),
                'wtd_wtd2': round(wtd_wtd2, 1),
                'wtd_wtd1': round(wtd_wtd1, 1),
                'd_d7': round(d_d7, 1),
                'd_d1': round(d_d1, 1),
                'd7': int(d7_val),
                'd2': int(d2_val),
                'd1': int(d1_val),
                'd': int(d_val)
            })
            
        total_wtd = sum(r['wtd'] for r in pivot_rows)
        total_wtd1 = sum(r['wtd1'] for r in pivot_rows)
        total_wtd2 = sum(r['wtd2'] for r in pivot_rows)
        total_d = sum(r['d'] for r in pivot_rows)
        total_d1 = sum(r['d1'] for r in pivot_rows)
        total_d2 = sum(r['d2'] for r in pivot_rows)
        total_d7 = sum(r['d7'] for r in pivot_rows)
        
        total_row = {
            'province': 'Tổng cộng',
            'wtd2': int(total_wtd2),
            'wtd1': int(total_wtd1),
            'wtd': int(total_wtd),
            'wtd_wtd2': round(((total_wtd - total_wtd2) / total_wtd2 * 100) if total_wtd2 > 0 else 0.0, 1),
            'wtd_wtd1': round(((total_wtd - total_wtd1) / total_wtd1 * 100) if total_wtd1 > 0 else 0.0, 1),
            'd_d7': round(((total_d - total_d7) / total_d7 * 100) if total_d7 > 0 else 0.0, 1),
            'd_d1': round(((total_d - total_d1) / total_d1 * 100) if total_d1 > 0 else 0.0, 1),
            'd7': int(total_d7),
            'd2': int(total_d2),
            'd1': int(total_d1),
            'd': int(total_d)
        }
        
        kpi_card_data = {
            'latest_date': latest_dt.strftime('%d-%m-%Y'),
            'today_vol': int(total_d),
            'd_d1': round(((total_d - total_d1) / total_d1 * 100) if total_d1 > 0 else 0.0, 1),
            'd_d7': round(((total_d - total_d7) / total_d7 * 100) if total_d7 > 0 else 0.0, 1)
        }
        
        # 3. Apply Date Range filter for the matrix and charts
        df_date_filtered = df_filtered.copy()
        if date_range == '7d':
            start_date = latest_dt - pd.Timedelta(days=6)
            df_date_filtered = df_date_filtered[(df_date_filtered['Date'] >= start_date) & (df_date_filtered['Date'] <= latest_dt)]
        elif date_range == '14d':
            start_date = latest_dt - pd.Timedelta(days=13)
            df_date_filtered = df_date_filtered[(df_date_filtered['Date'] >= start_date) & (df_date_filtered['Date'] <= latest_dt)]
        elif date_range == '30d':
            start_date = latest_dt - pd.Timedelta(days=29)
            df_date_filtered = df_date_filtered[(df_date_filtered['Date'] >= start_date) & (df_date_filtered['Date'] <= latest_dt)]
            
        # Get list of unique dates for matrix and charts
        matrix_dates = sorted(df_date_filtered['Date'].dt.strftime('%Y-%m-%d').unique())
        
        # 4. Compute Matrix Heatmap Data
        matrix_rows = []
        if len(matrix_dates) > 0 and len(df_date_filtered) > 0:
            prov_date_vol = df_date_filtered.groupby(['Tỉnh', df_date_filtered['Date'].dt.strftime('%Y-%m-%d')])['Volume'].sum().unstack(fill_value=0)
            po_date_vol = df_date_filtered.groupby(['Tỉnh', 'Bưu cục', df_date_filtered['Date'].dt.strftime('%Y-%m-%d')])['Volume'].sum().unstack(fill_value=0)
            
            # Ensure all columns exist for all dates
            for d in matrix_dates:
                if d not in prov_date_vol.columns:
                    prov_date_vol[d] = 0
                if d not in po_date_vol.columns:
                    po_date_vol[d] = 0
                    
            for p in sorted(df_date_filtered['Tỉnh'].dropna().unique()):
                p_vols = prov_date_vol.loc[p].to_dict() if p in prov_date_vol.index else {}
                p_total = int(sum(p_vols.values()))
                
                pos_list = []
                if p in po_date_vol.index:
                    p_po_df = po_date_vol.loc[p]
                    for po in sorted(p_po_df.index):
                        po_vols = p_po_df.loc[po].to_dict()
                        po_total = int(sum(po_vols.values()))
                        pos_list.append({
                            'bc': po,
                            'data': {d: int(po_vols.get(d, 0)) for d in matrix_dates},
                            'total': po_total
                        })
                
                matrix_rows.append({
                    'province': p,
                    'data': {d: int(p_vols.get(d, 0)) for d in matrix_dates},
                    'total': p_total,
                    'pos': pos_list
                })
                
        # 5. Customer Group Line Chart Series
        line_series = []
        if len(matrix_dates) > 0 and len(df_date_filtered) > 0:
            cust_daily = df_date_filtered.groupby([df_date_filtered['Date'].dt.strftime('%Y-%m-%d'), 'Khách hàng'])['Volume'].sum().unstack(fill_value=0)
            standard_customers = ['SME', 'Shopee-nhỏ', 'TTS-nhỏ', 'Shopee-Bulky', 'Khác']
            for c in standard_customers:
                if c in cust_daily.columns:
                    c_data = [int(x) for x in cust_daily[c].tolist()]
                else:
                    c_data = [0] * len(matrix_dates)
                line_series.append({
                    'name': c,
                    'data': c_data
                })
                
        # 6. Grouped Bar Chart by Province Series
        bar_series = []
        if len(matrix_dates) > 0 and len(df_date_filtered) > 0:
            prov_daily = df_date_filtered.groupby([df_date_filtered['Date'].dt.strftime('%Y-%m-%d'), 'Tỉnh'])['Volume'].sum().unstack(fill_value=0)
            for p in provinces_list:
                if p in prov_daily.columns:
                    p_data = [int(x) for x in prov_daily[p].tolist()]
                else:
                    p_data = [0] * len(matrix_dates)
                bar_series.append({
                    'name': p,
                    'data': p_data
                })
                
        # 7. Treemap Data sorted by Absolute 7D Growth
        treemap_list = []
        # We compute D vs D-7. D is the latest date in df_filtered, D-7 is latest_dt - 7 days.
        df_d = df_filtered[df_filtered['Date'] == latest_dt]
        df_d7 = df_filtered[df_filtered['Date'] == (latest_dt - pd.Timedelta(days=7))]
        
        if len(df_d) > 0:
            vol_d = df_d.groupby(['Tỉnh', 'Bưu cục'])['Volume'].sum().reset_index()
            vol_d7 = df_d7.groupby('Bưu cục')['Volume'].sum().reset_index()
            
            merged_growth = pd.merge(vol_d, vol_d7, on='Bưu cục', suffixes=('_d', '_d7'), how='left').fillna(0)
            merged_growth['growth_abs'] = merged_growth['Volume_d'] - merged_growth['Volume_d7']
            merged_growth['growth_pct'] = (merged_growth['growth_abs'] / merged_growth['Volume_d7'] * 100).replace([np.inf, -np.inf], 0).fillna(0)
            
            # Sort by absolute growth descending
            merged_growth = merged_growth.sort_values(by='growth_abs', ascending=False)
            
            for _, row in merged_growth.iterrows():
                treemap_list.append({
                    'name': row['Bưu cục'],
                    'value': int(row['Volume_d']),
                    'province': row['Tỉnh'],
                    'growth_abs': int(row['growth_abs']),
                    'growth_pct': round(float(row['growth_pct']), 1)
                })
                
        return jsonify(clean_nan({
            "kpi": kpi_card_data,
            "table": pivot_rows,
            "total": total_row,
            "filters": {
                "provinces": provinces_opt,
                "districts": districts_opt,
                "wards": wards_opt,
                "post_offices": post_offices_opt,
                "customers": customers_opt,
                "po_types": po_types_opt
            },
            "matrix": {
                "dates": matrix_dates,
                "rows": matrix_rows
            },
            "charts": {
                "line": {
                    "dates": matrix_dates,
                    "series": line_series
                },
                "bar": {
                    "dates": matrix_dates,
                    "series": bar_series
                },
                "treemap": treemap_list
            }
        }))
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Lỗi xử lý báo cáo volume tạo đơn: {str(e)}"}), 500

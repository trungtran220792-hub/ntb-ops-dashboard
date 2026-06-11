import os
import sys
import time
import pandas as pd

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import get_dataframes, apply_filters, get_week_label, get_week_range_str, clean_str_key

def format_kpi_dict(latest_kpi, prev_kpi, lw_kpi, w1_kpi=None, w2_kpi=None, prev_date_label='Ngày trước', n3_kpi=None, n3_date_label=None):
    res = {
        'ltc': latest_kpi['ltc'] if latest_kpi else 0.0,
        'gtc': latest_kpi['gtc'] if latest_kpi else 0.0,
        'ttc': latest_kpi['ttc'] if latest_kpi else 0.0,
        'vol_ltc': latest_kpi['vol_ltc'] if latest_kpi else 0,
        'vol_gtc': latest_kpi['vol_gtc'] if latest_kpi else 0
    }
    if latest_kpi:
        if prev_kpi:
            res['dod'] = {
                'ltc': round(latest_kpi['ltc'] - prev_kpi['ltc'], 2),
                'gtc': round(latest_kpi['gtc'] - prev_kpi['gtc'], 2),
                'ttc': round(latest_kpi['ttc'] - prev_kpi['ttc'], 2),
                'prev_date_str': prev_date_label,
                'prev_ltc': prev_kpi['ltc'],
                'prev_gtc': prev_kpi['gtc'],
                'prev_ttc': prev_kpi['ttc']
            }
        else:
            res['dod'] = None
            
        if lw_kpi:
            res['wow'] = {
                'ltc': round(latest_kpi['ltc'] - lw_kpi['ltc'], 2),
                'gtc': round(latest_kpi['gtc'] - lw_kpi['gtc'], 2),
                'ttc': round(latest_kpi['ttc'] - lw_kpi['ttc'], 2),
                'lw_ltc': lw_kpi['ltc'],
                'lw_gtc': lw_kpi['gtc'],
                'lw_ttc': lw_kpi['ttc']
            }
        else:
            res['wow'] = None
            
        if n3_kpi:
            n3_label = n3_date_label.split(' - ')[1] if (n3_date_label and ' - ' in n3_date_label) else '3 ngày trước'
            res['n3'] = {
                'ltc': round(latest_kpi['ltc'] - n3_kpi['ltc'], 2),
                'gtc': round(latest_kpi['gtc'] - n3_kpi['gtc'], 2),
                'ttc': round(latest_kpi['ttc'] - n3_kpi['ttc'], 2),
                'n3_ltc': n3_kpi['ltc'],
                'n3_gtc': n3_kpi['gtc'],
                'n3_ttc': n3_kpi['ttc'],
                'n3_date_str': n3_label
            }
        else:
            res['n3'] = None
    else:
        res['dod'] = None
        res['wow'] = None
        res['n3'] = None
        
    if w1_kpi:
        res['w1_avg'] = {
            'ltc': w1_kpi['ltc'],
            'gtc': w1_kpi['gtc'],
            'ttc': w1_kpi['ttc'],
            'days_count': 7
        }
    else:
        res['w1_avg'] = None
        
    if w2_kpi:
        res['w2_avg'] = {
            'ltc': w2_kpi['ltc'],
            'gtc': w2_kpi['gtc'],
            'ttc': w2_kpi['ttc'],
            'days_count': 7
        }
        res['wow_avg'] = {
            'ltc': round(w1_kpi['ltc'] - w2_kpi['ltc'], 2),
            'gtc': round(w1_kpi['gtc'] - w2_kpi['gtc'], 2),
            'ttc': round(w1_kpi['ttc'] - w2_kpi['ttc'], 2)
        }
    else:
        res['w2_avg'] = None
        res['wow_avg'] = None
        
    return res

def profile():
    log_lines = []
    
    # 1. Measure dataframes loading
    start = time.time()
    df_gtc, df_ltc, df_aging, df_treo = get_dataframes(force=False)
    log_lines.append(f"1. Loading dataframes took: {time.time() - start:.2f}s")
    
    # 2. Time Group = ngay
    start = time.time()
    all_times = set(df_gtc['Time'].dropna().unique()).union(set(df_ltc['Time'].dropna().unique()))
    dates_sorted = sorted(list(all_times), key=lambda x: pd.to_datetime(x.split(' - ')[0]))
    latest_date = dates_sorted[-1]
    idx = dates_sorted.index(latest_date)
    prev_date = dates_sorted[idx - 1] if idx >= 1 else None
    
    latest_dt = pd.to_datetime(latest_date.split(' - ')[0])
    last_week_date = None
    for d in dates_sorted[:idx]:
        dt = pd.to_datetime(d.split(' - ')[0])
        if (latest_dt - dt).days == 7:
            last_week_date = d
            break
            
    n3_date = None
    for d in dates_sorted[:idx]:
        dt = pd.to_datetime(d.split(' - ')[0])
        if (latest_dt - dt).days == 3:
            n3_date = d
            break
    if not n3_date and idx >= 3:
        n3_date = dates_sorted[idx - 3]
        
    week1_dates = dates_sorted[max(0, idx-6):idx+1]
    week2_dates = dates_sorted[max(0, idx-13):max(0, idx-6)]
    log_lines.append(f"2. Basic date sorting/finding took: {time.time() - start:.4f}s")
    
    # 3. Helper functions benchmark
    def compute_kpi_for_date(date_str, filter_am=None, filter_prov=None, filter_po=None):
        gtc_d = df_gtc[df_gtc['Time'] == date_str]
        ltc_d = df_ltc[df_ltc['Time'] == date_str]
        gtc_d = apply_filters(gtc_d, filter_am, filter_prov, filter_po)
        ltc_d = apply_filters(ltc_d, filter_am, filter_prov, filter_po)
        ltc_vol = ltc_d['Volume'].sum()
        ltc_done = ltc_d['ltc_vol'].sum()
        gtc_vol = gtc_d['Volume'].sum()
        gtc_done = gtc_d['delivered_vol'].sum()
        ttc_done = gtc_d['ttc_vol'].sum()
        return {
            'ltc': round((ltc_done / ltc_vol * 100), 2) if ltc_vol > 0 else 0.0,
            'gtc': round((gtc_done / gtc_vol * 100), 2) if gtc_vol > 0 else 0.0,
            'ttc': round((ttc_done / gtc_vol * 100), 2) if gtc_vol > 0 else 0.0,
            'vol_ltc': int(ltc_vol),
            'vol_gtc': int(gtc_vol)
        }
        
    def compute_kpi_for_date_range(dates_list, filter_am=None, filter_prov=None, filter_po=None):
        gtc_d = df_gtc[df_gtc['Time'].isin(dates_list)]
        ltc_d = df_ltc[df_ltc['Time'].isin(dates_list)]
        gtc_d = apply_filters(gtc_d, filter_am, filter_prov, filter_po)
        ltc_d = apply_filters(ltc_d, filter_am, filter_prov, filter_po)
        ltc_vol = ltc_d['Volume'].sum()
        ltc_done = ltc_d['ltc_vol'].sum()
        gtc_vol = gtc_d['Volume'].sum()
        gtc_done = gtc_d['delivered_vol'].sum()
        ttc_done = gtc_d['ttc_vol'].sum()
        return {
            'ltc': round((ltc_done / ltc_vol * 100), 2) if ltc_vol > 0 else 0.0,
            'gtc': round((gtc_done / gtc_vol * 100), 2) if gtc_vol > 0 else 0.0,
            'ttc': round((ttc_done / gtc_vol * 100), 2) if gtc_vol > 0 else 0.0,
            'vol_ltc': int(ltc_vol),
            'vol_gtc': int(gtc_vol)
        }

    start = time.time()
    overall_latest = compute_kpi_for_date(latest_date)
    overall_prev = compute_kpi_for_date(prev_date) if prev_date else None
    overall_lw = compute_kpi_for_date(last_week_date) if last_week_date else None
    overall_w1 = compute_kpi_for_date_range(week1_dates)
    overall_w2 = compute_kpi_for_date_range(week2_dates) if week2_dates else None
    overall_n3 = compute_kpi_for_date(n3_date) if n3_date else None
    log_lines.append(f"3. Overall KPIs calculation took: {time.time() - start:.4f}s")
    
    # 4. Province KPIs calculation (the loop)
    start = time.time()
    all_provinces = set(df_ltc['mapped_prov'].unique()).union(set(df_gtc['mapped_prov'].unique()))
    
    kpis = {}
    for prov_name in all_provinces:
        if prov_name == "Không xác định":
            continue
        prov_start = time.time()
        prov_latest = compute_kpi_for_date(latest_date, None, prov_name, None)
        prov_prev = compute_kpi_for_date(prev_date, None, prov_name, None) if prev_date else None
        prov_lw = compute_kpi_for_date(last_week_date, None, prov_name, None) if last_week_date else None
        prov_w1 = compute_kpi_for_date_range(week1_dates, None, prov_name, None)
        prov_w2 = compute_kpi_for_date_range(week2_dates, None, prov_name, None) if week2_dates else None
        prov_n3 = compute_kpi_for_date(n3_date, None, prov_name, None) if n3_date else None
        clean_key = clean_str_key(prov_name)
        kpis[clean_key] = format_kpi_dict(prov_latest, prov_prev, prov_lw, prov_w1, prov_w2, "Ngày trước", prov_n3, n3_date)
        kpis[clean_key]['name'] = prov_name
        
    log_lines.append(f"4. Total Provinces loop took: {time.time() - start:.4f}s")
    
    # 5. Province tables and backlog grouping
    start = time.time()
    today_gtc = df_gtc[df_gtc['Time'] == latest_date]
    today_ltc = df_ltc[df_ltc['Time'] == latest_date]
    gtc_prov = today_gtc.groupby('mapped_prov').agg({'Volume': 'sum', 'delivered_vol': 'sum', 'ttc_vol': 'sum'}).reset_index()
    ltc_prov = today_ltc.groupby('mapped_prov').agg({'Volume': 'sum', 'ltc_vol': 'sum'}).reset_index()
    merged_prov = pd.merge(gtc_prov, ltc_prov, on='mapped_prov', suffixes=('_gtc', '_ltc'), how='outer').fillna(0)
    log_lines.append(f"5. Province grouping tables took: {time.time() - start:.4f}s")

    with open('scratch/profile_summary_res.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(log_lines))
    print("Done profiling and wrote to scratch/profile_summary_res.txt")

if __name__ == '__main__':
    profile()

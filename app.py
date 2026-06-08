import os
from dotenv import load_dotenv
load_dotenv()
import json
import datetime
import pandas as pd
import numpy as np
from flask import Flask, jsonify, render_template, request, Response
import threading
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import re
import requests

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['TEMPLATES_AUTO_RELOAD'] = True
CACHE_LOCK = threading.RLock()

# PBKDF2:SHA256 hash of 'admin123' and 'staff123'
PASSWORD_HASH = generate_password_hash('admin123', method='pbkdf2:sha256')
STAFF_PASSWORD_HASH = generate_password_hash('staff123', method='pbkdf2:sha256')

def check_auth(username, password):
    if username == 'admin' and check_password_hash(PASSWORD_HASH, password):
        return 'admin'
    elif username == 'staff' and check_password_hash(STAFF_PASSWORD_HASH, password):
        return 'staff'
    return None

def is_admin():
    auth = request.authorization
    return auth and auth.username == 'admin'

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return Response(
                'Yêu cầu đăng nhập để truy cập hệ thống.', 401,
                {'WWW-Authenticate': 'Basic realm="Dashboard Login Required"'}
            )
        return f(*args, **kwargs)
    return decorated

import functools
def with_lock(lock):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)
        return wrapper
    return decorator

@app.after_request
def add_security_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    
    # Disable caching to force updates
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    # Secure HTTP headers from rules
    response.headers['Content-Security-Policy'] = "default-src 'self' http://127.0.0.1:5000; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://unpkg.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com https://unpkg.com; font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; img-src 'self' data: https://*.basemaps.cartocdn.com https://unpkg.com; connect-src 'self' http://127.0.0.1:5000;"
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    response.headers.pop('X-Powered-By', None)
    return response
WORKSPACE_DIR = os.getcwd()
HISTORY_FILE = os.path.join(WORKSPACE_DIR, 'backlog_history.json')
CONFIG_FILE = os.path.join(WORKSPACE_DIR, 'config.json')

def load_config():
    defaults = {
        "ops_url": os.environ.get("OPS_URL", ""),
        "opr_url": os.environ.get("OPR_URL", ""),
        "aging_url": os.environ.get("AGING_URL", ""),
        "treo_url": os.environ.get("TREO_URL", ""),
        "bat_on_url": os.environ.get("BAT_ON_URL", ""),
        "off_spe_url": os.environ.get("OFF_SPE_URL", ""),
        "tao_don_url": os.environ.get("TAO_DON_URL", "")
    }
    
    config = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except Exception as e:
            print(f"Error loading config.json: {e}")
            
    final_config = {}
    keys_map = {
        "ops_url": "OPS_URL",
        "opr_url": "OPR_URL",
        "aging_url": "AGING_URL",
        "treo_url": "TREO_URL",
        "bat_on_url": "BAT_ON_URL",
        "off_spe_url": "OFF_SPE_URL",
        "tao_don_url": "TAO_DON_URL"
    }
    for k, env_name in keys_map.items():
        val = os.environ.get(env_name, "")
        if not val.strip():
            val = config.get(k, "")
        final_config[k] = val.strip()
        
    return final_config

def save_config(config):
    try:
        clean_config = {
            "ops_url": config.get("ops_url", "").strip(),
            "opr_url": config.get("opr_url", "").strip(),
            "aging_url": config.get("aging_url", "").strip(),
            "treo_url": config.get("treo_url", "").strip(),
            "bat_on_url": config.get("bat_on_url", "").strip(),
            "off_spe_url": config.get("off_spe_url", "").strip(),
            "tao_don_url": config.get("tao_don_url", "").strip()
        }
        
        # 1. Update in-memory os.environ
        keys_map = {
            "ops_url": "OPS_URL",
            "opr_url": "OPR_URL",
            "aging_url": "AGING_URL",
            "treo_url": "TREO_URL",
            "bat_on_url": "BAT_ON_URL",
            "off_spe_url": "OFF_SPE_URL",
            "tao_don_url": "TAO_DON_URL"
        }
        for k, env_name in keys_map.items():
            os.environ[env_name] = clean_config[k]
            
        # 2. Update .env file if it exists, otherwise update config.json
        env_file = os.path.join(WORKSPACE_DIR, '.env')
        if os.path.exists(env_file):
            lines = []
            with open(env_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            new_lines = []
            keys_written = set()
            for line in lines:
                matched = False
                for k, env_name in keys_map.items():
                    if line.strip().startswith(f"{env_name}="):
                        new_lines.append(f'{env_name}="{clean_config[k]}"\n')
                        keys_written.add(env_name)
                        matched = True
                        break
                if not matched:
                    new_lines.append(line)
                    
            for k, env_name in keys_map.items():
                if env_name not in keys_written:
                    new_lines.append(f'{env_name}="{clean_config[k]}"\n')
                    
            with open(env_file, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
        else:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(clean_config, f, indent=4, ensure_ascii=False)
                
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def download_google_sheet(url, output_path):
    if not url or not url.strip():
        return True, "Không có link, sử dụng file local."
        
    url = url.strip()
    if not (url.startswith("https://docs.google.com/spreadsheets/") or url.startswith("http://docs.google.com/spreadsheets/")):
        return False, "Link không hợp lệ. Phải bắt đầu bằng https://docs.google.com/spreadsheets/"
        
    match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
    if not match:
        return False, "Không tìm thấy Spreadsheet ID hợp lệ trong link."
        
    spreadsheet_id = match.group(1)
    export_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=xlsx"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        }
        response = requests.get(export_url, headers=headers, timeout=60)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True, "Tải thành công."
        else:
            return False, f"Tải thất bại (Mã lỗi: {response.status_code}). Vui lòng kiểm tra quyền chia sẻ link (phải để ở chế độ 'Người có liên kết có quyền xem')."
    except Exception as e:
        return False, mask_url(f"Lỗi kết nối khi tải: {str(e)}")

# Helper function to clean strings for merge
def clean_str(val):
    if pd.isna(val):
        return ""
    return str(val).strip().lower()

def safe_divide(a, b):
    if b == 0:
        return 0.0
    return round((a / b) * 100, 2)

def clean_nan(obj):
    if isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nan(x) for x in obj]
    elif isinstance(obj, float):
        if np.isnan(obj) or np.isinf(obj):
            return None
    elif pd.isna(obj):
        return None
    return obj

def read_ops_sheet(xls, sheet_type):
    sheet_names_lower = [s.strip().lower() for s in xls.sheet_names]
    
    if sheet_type == "gtc":
        for candidate in ["datagtc", "data"]:
            if candidate in sheet_names_lower:
                idx = sheet_names_lower.index(candidate)
                df = pd.read_excel(xls, sheet_name=xls.sheet_names[idx])
                
                # Normalize column names in df to standard GTC ones
                cols_lower = {c.strip().lower(): c for c in df.columns}
                rename_map = {}
                core_gtc_cols = {
                    'cấp quản lý': 'Cấp Quản Lý',
                    'chi tiết': 'Chi tiết',
                    'loại hàng': 'Loại Hàng',
                    'time': 'Time',
                    'volume': 'Volume',
                    '% gán': '% Gán',
                    '% gtc': '% GTC',
                    '% chuyển trả': '% Chuyển trả',
                    'leadtime': 'Leadtime',
                    'am': 'AM',
                    'tỉnh': 'Tỉnh'
                }
                for k, standard_name in core_gtc_cols.items():
                    if k in cols_lower and cols_lower[k] != standard_name:
                        rename_map[cols_lower[k]] = standard_name
                if rename_map:
                    df = df.rename(columns=rename_map)
                return df
        raise ValueError(f"Không tìm thấy sheet GTC (cần Datagtc hoặc Data) trong file. Các sheet hiện có: {xls.sheet_names}")
        
    elif sheet_type == "ltc":
        # First priority: look for dataltc, rawltc, datalts, ltc
        for candidate in ["dataltc", "rawltc", "datalts", "ltc"]:
            if candidate in sheet_names_lower:
                idx = sheet_names_lower.index(candidate)
                df = pd.read_excel(xls, sheet_name=xls.sheet_names[idx])
                
                cols_lower = {c.strip().lower(): c for c in df.columns}
                rename_map = {}
                
                # Normalize core columns
                core_ltc_cols = {
                    'cấp quản lý': 'Cấp quản lý',
                    'chi tiết': 'Chi tiết',
                    'ca': 'Ca',
                    'time': 'Time',
                    'volume': 'Volume',
                    'leadtime': 'Leadtime'
                }
                for k, standard_name in core_ltc_cols.items():
                    if k in cols_lower and cols_lower[k] != standard_name:
                        rename_map[cols_lower[k]] = standard_name
                        
                # Rename `% gtc` -> `%LTC` or `% ltc` -> `%LTC` if %ltc is not present
                if '%ltc' not in cols_lower:
                    if '% ltc' in cols_lower:
                        rename_map[cols_lower['% ltc']] = '%LTC'
                    elif '% gtc' in cols_lower:
                        rename_map[cols_lower['% gtc']] = '%LTC'
                else:
                    rename_map[cols_lower['%ltc']] = '%LTC'
                    
                # Rename `% lc` -> `%LC` or `% chuyển trả` -> `%LC` if %lc is not present
                if '%lc' not in cols_lower:
                    if '% lc' in cols_lower:
                        rename_map[cols_lower['% lc']] = '%LC'
                    elif '% chuyển trả' in cols_lower:
                        rename_map[cols_lower['% chuyển trả']] = '%LC'
                else:
                    rename_map[cols_lower['%lc']] = '%LC'
                    
                # Rename `% gán` -> `%Gán` if %gán is not present
                if '%gán' not in cols_lower:
                    if '% gán' in cols_lower:
                        rename_map[cols_lower['% gán']] = '%Gán'
                else:
                    rename_map[cols_lower['%gán']] = '%Gán'
                    
                if rename_map:
                    df = df.rename(columns=rename_map)
                return df
                
        # Second priority fallback: any sheet with "ltc" in its name
        for s in xls.sheet_names:
            if "ltc" in s.lower():
                df = pd.read_excel(xls, sheet_name=s)
                cols_lower = {c.strip().lower(): c for c in df.columns}
                rename_map = {}
                
                # Normalize core columns
                core_ltc_cols = {
                    'cấp quản lý': 'Cấp quản lý',
                    'chi tiết': 'Chi tiết',
                    'ca': 'Ca',
                    'time': 'Time',
                    'volume': 'Volume',
                    'leadtime': 'Leadtime'
                }
                for k, standard_name in core_ltc_cols.items():
                    if k in cols_lower and cols_lower[k] != standard_name:
                        rename_map[cols_lower[k]] = standard_name
                        
                if '%ltc' not in cols_lower:
                    if '% ltc' in cols_lower:
                        rename_map[cols_lower['% ltc']] = '%LTC'
                    elif '% gtc' in cols_lower:
                        rename_map[cols_lower['% gtc']] = '%LTC'
                else:
                    rename_map[cols_lower['%ltc']] = '%LTC'
                    
                if '%lc' not in cols_lower:
                    if '% lc' in cols_lower:
                        rename_map[cols_lower['% lc']] = '%LC'
                    elif '% chuyển trả' in cols_lower:
                        rename_map[cols_lower['% chuyển trả']] = '%LC'
                else:
                    rename_map[cols_lower['%lc']] = '%LC'
                    
                if '%gán' not in cols_lower:
                    if '% gán' in cols_lower:
                        rename_map[cols_lower['% gán']] = '%Gán'
                else:
                    rename_map[cols_lower['%gán']] = '%Gán'
                    
                if rename_map:
                    df = df.rename(columns=rename_map)
                return df
                
        raise ValueError(f"Không tìm thấy sheet LTC (cần Dataltc hoặc rawltc hoặc DataLTC) trong file. Các sheet hiện có: {xls.sheet_names}")
        
    elif sheet_type == "co_cau":
        for candidate in ["cơ cấu", "co cau"]:
            if candidate in sheet_names_lower:
                idx = sheet_names_lower.index(candidate)
                return pd.read_excel(xls, sheet_name=xls.sheet_names[idx])
        raise ValueError(f"Không tìm thấy sheet Cơ cấu trong file. Các sheet hiện có: {xls.sheet_names}")

# ==========================================
# 1. PROCESS OPERATIONAL REPORT
# ==========================================
def process_operational_report(df_gtc=None, df_ltc=None):
    file_path = os.path.join(WORKSPACE_DIR, 'Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx')
    
    try:
        if df_gtc is None or df_ltc is None:
            if not os.path.exists(file_path):
                return {"error": f"Không tìm thấy file: {os.path.basename(file_path)}"}
            with pd.ExcelFile(file_path) as xls:
                if df_gtc is None:
                    df_gtc = read_ops_sheet(xls, "gtc")
                if df_ltc is None:
                    df_ltc = read_ops_sheet(xls, "ltc")
        
        df_gtc = df_gtc.dropna(subset=["Volume"]).copy()
        df_gtc['Leadtime'] = pd.to_numeric(df_gtc['Leadtime'], errors='coerce')
        
        df_ltc = df_ltc.dropna(subset=["Volume"]).copy()
        df_ltc['Leadtime'] = pd.to_numeric(df_ltc['Leadtime'], errors='coerce')
        
        # Calculate overall metrics
        df_gtc['delivered_vol'] = df_gtc['Volume'] * df_gtc['% GTC']
        df_gtc['assigned_vol'] = df_gtc['Volume'] * df_gtc['% Gán']
        df_gtc['return_vol'] = df_gtc['Volume'] * df_gtc['% Chuyển trả']
        df_ltc['ltc_vol'] = df_ltc['Volume'] * df_ltc['%LTC']
        
        # Determine the latest date dynamically from Time column safely
        latest_date_gtc = None
        if 'Time' in df_gtc.columns and len(df_gtc) > 0:
            times = df_gtc['Time'].dropna().unique()
            try:
                dates_sorted = sorted(times, key=lambda x: pd.to_datetime(str(x).split(' - ')[0]))
                if dates_sorted:
                    latest_date_gtc = dates_sorted[-1]
            except Exception as e:
                print(f"Error sorting GTC dates: {e}")
                if len(times) > 0:
                    latest_date_gtc = times[-1]
                    
        latest_date_ltc = None
        if 'Time' in df_ltc.columns and len(df_ltc) > 0:
            times = df_ltc['Time'].dropna().unique()
            try:
                dates_sorted = sorted(times, key=lambda x: pd.to_datetime(str(x).split(' - ')[0]))
                if dates_sorted:
                    latest_date_ltc = dates_sorted[-1]
            except Exception as e:
                print(f"Error sorting LTC dates: {e}")
                if len(times) > 0:
                    latest_date_ltc = times[-1]
                    
        df_gtc_latest = df_gtc[df_gtc['Time'] == latest_date_gtc] if latest_date_gtc else df_gtc
        df_ltc_latest = df_ltc[df_ltc['Time'] == latest_date_ltc] if latest_date_ltc else df_ltc
        
        total_vol = float(df_gtc_latest['Volume'].sum())
        total_gtc_vol = float(df_gtc_latest['delivered_vol'].sum())
        total_assigned_vol = float(df_gtc_latest['assigned_vol'].sum())
        total_return_vol = float(df_gtc_latest['return_vol'].sum())
        total_inventory_vol = float((df_gtc_latest['Volume'] - df_gtc_latest['delivered_vol'] - df_gtc_latest['return_vol']).sum()) # rough estimate of tồn
        
        overall_gtc = safe_divide(total_gtc_vol, total_vol)
        overall_gan = safe_divide(total_assigned_vol, total_vol)
        
        # Calculate LTC metrics
        total_ltc_vol = float(df_ltc_latest['Volume'].sum())
        total_on_ltc_vol = float(df_ltc_latest['ltc_vol'].sum())
        overall_ltc = safe_divide(total_on_ltc_vol, total_ltc_vol)
        
        # Average Leadtime
        avg_leadtime = float(df_gtc_latest['Leadtime'].mean())
        
        # Shift breakdown (Ca 1, Ca 2, Tồn) in Datagtc
        ca1_vol = float(df_gtc_latest[df_gtc_latest['Loại Hàng'] == 'Hàng Mới Ca 1']['Volume'].sum())
        ca2_vol = float(df_gtc_latest[df_gtc_latest['Loại Hàng'] == 'Hàng Mới Ca 2']['Volume'].sum())
        ton_vol = float(df_gtc_latest[df_gtc_latest['Loại Hàng'] == 'Hàng Tồn']['Volume'].sum())
        new_vol = ca1_vol + ca2_vol
        
        # Top 10 Best and Worst Post Offices by GTC
        po_gtc = df_gtc.groupby('Chi tiết').agg({'Volume': 'sum', 'delivered_vol': 'sum', 'Leadtime': 'mean'}).reset_index()
        po_gtc['% GTC'] = (po_gtc['delivered_vol'] / po_gtc['Volume']) * 100
        po_gtc = po_gtc[po_gtc['Volume'] >= 100] # filter out small volumes for ranking
        
        top_10_gtc = po_gtc.sort_values(by='% GTC', ascending=False).head(10).to_dict(orient='records')
        worst_10_gtc = po_gtc.sort_values(by='% GTC', ascending=True).head(10).to_dict(orient='records')
        
        # Top 10 Best and Worst Post Offices by LTC
        po_ltc = df_ltc.groupby('Chi tiết').agg({'Volume': 'sum', 'ltc_vol': 'sum', 'Leadtime': 'mean'}).reset_index()
        po_ltc['% LTC'] = (po_ltc['ltc_vol'] / po_ltc['Volume']) * 100
        po_ltc = po_ltc[po_ltc['Volume'] >= 100]
        
        top_10_ltc = po_ltc.sort_values(by='% LTC', ascending=False).head(10).to_dict(orient='records')
        worst_10_ltc = po_ltc.sort_values(by='% LTC', ascending=True).head(10).to_dict(orient='records')
        
        # Xu hướng GTC & Volume theo ngày
        trend_gtc = df_gtc.groupby('Time').agg({'Volume': 'sum', 'delivered_vol': 'sum'}).reset_index()
        trend_gtc['% GTC'] = (trend_gtc['delivered_vol'] / trend_gtc['Volume']) * 100
        trend_gtc_list = trend_gtc.sort_values('Time').to_dict(orient='records')
        
        # Xu hướng LTC theo ngày
        trend_ltc = df_ltc.groupby('Time').agg({'Volume': 'sum', 'ltc_vol': 'sum'}).reset_index()
        trend_ltc['% LTC'] = (trend_ltc['ltc_vol'] / trend_ltc['Volume']) * 100
        trend_ltc_list = trend_ltc.sort_values('Time').to_dict(orient='records')
        
        return {
            "total_volume": int(total_vol),
            "overall_gtc": overall_gtc,
            "overall_gan": overall_gan,
            "overall_ltc": overall_ltc,
            "avg_leadtime": round(avg_leadtime, 2),
            "ca1_vol": int(ca1_vol),
            "ca2_vol": int(ca2_vol),
            "ton_vol": int(ton_vol),
            "new_vol": int(new_vol),
            "top_10_gtc": top_10_gtc,
            "worst_10_gtc": worst_10_gtc,
            "top_10_ltc": top_10_ltc,
            "worst_10_ltc": worst_10_ltc,
            "trend_gtc": trend_gtc_list,
            "trend_ltc": trend_ltc_list
        }
    except Exception as e:
        return {"error": f"Lỗi xử lý file báo cáo vận hành: {str(e)}"}

# ==========================================
# 2. PROCESS OPR TTS REPORT
# ==========================================
def process_opr_report(df_opr=None, df_oe=None, df_rawopr=None):
    file_path = os.path.join(WORKSPACE_DIR, 'OPR TTS.xlsx')
    
    try:
        if df_opr is None or df_oe is None or df_rawopr is None:
            if not os.path.exists(file_path):
                return {"error": f"Không tìm thấy file OPR: {os.path.basename(file_path)}"}
            with pd.ExcelFile(file_path) as xls:
                if df_opr is None:
                    df_opr = pd.read_excel(xls, sheet_name="OPR")
                if df_oe is None:
                    df_oe = pd.read_excel(xls, sheet_name="OE_madh")
                if df_rawopr is None and "rawopr" in xls.sheet_names:
                    df_rawopr = pd.read_excel(xls, sheet_name="rawopr")
        
        df_opr = df_opr.dropna(subset=["vol_ltc"]).copy()
        
        # Calculate OPR Overall
        total_vol = float(df_opr['vol_ltc'].sum())
        total_ot = float(df_opr['ot'].sum())
        overall_opr = safe_divide(total_ot, total_vol)
        
        # Calculate OPR comparisons (n-1 and cùng kỳ thứ)
        opr_n1 = None
        opr_wk = None
        delta_n1 = None
        delta_wk = None
        
        if df_rawopr is not None and not df_rawopr.empty:
            try:
                # Normalize dates to YYYY-MM-DD
                df_opr_dates = pd.to_datetime(df_opr['NgayLTC'], errors='coerce').dt.strftime('%Y-%m-%d')
                df_rawopr_dates = pd.to_datetime(df_rawopr['NgayLTC'], errors='coerce').dt.strftime('%Y-%m-%d')
                
                valid_dates = df_opr_dates.dropna().unique()
                if len(valid_dates) > 0:
                    report_date_str = max(valid_dates)
                    report_dt = pd.to_datetime(report_date_str)
                    
                    n1_date_str = (report_dt - pd.Timedelta(days=1)).strftime('%Y-%m-%d')
                    wk_date_str = (report_dt - pd.Timedelta(days=7)).strftime('%Y-%m-%d')
                    
                    # Create temporary date columns
                    df_opr_temp = df_opr.copy()
                    df_rawopr_temp = df_rawopr.copy()
                    df_opr_temp['NgayLTC_str'] = df_opr_dates
                    df_rawopr_temp['NgayLTC_str'] = df_rawopr_dates
                    
                    cols = ['NgayLTC_str', 'vol_ltc', 'ot']
                    df_comb = pd.concat([df_opr_temp[cols], df_rawopr_temp[cols]], ignore_index=True)
                    df_comb = df_comb.dropna(subset=['NgayLTC_str', 'vol_ltc', 'ot'])
                    
                    def get_opr_for_date(df, date_str):
                        df_date = df[df['NgayLTC_str'] == date_str]
                        if len(df_date) == 0:
                            return None
                        t_vol = float(df_date['vol_ltc'].sum())
                        t_ot = float(df_date['ot'].sum())
                        return safe_divide(t_ot, t_vol)
                    
                    opr_n1 = get_opr_for_date(df_comb, n1_date_str)
                    opr_wk = get_opr_for_date(df_comb, wk_date_str)
                    
                    if opr_n1 is not None:
                        delta_n1 = round(overall_opr - opr_n1, 2)
                    if opr_wk is not None:
                        delta_wk = round(overall_opr - opr_wk, 2)
            except Exception as ex:
                print(f"Lỗi tính toán OPR so sánh: {ex}")
        
        # Calculate OPR by Creation Time Slot (Khung giờ tạo)
        time_slot_col = 'Khung giờ tạo' if 'Khung giờ tạo' in df_opr.columns else 'khung_gio_tao_don'
        slot_opr = df_opr.groupby(time_slot_col).agg({'vol_ltc': 'sum', 'ot': 'sum'}).reset_index()
        slot_opr['% OPR'] = (slot_opr['ot'] / slot_opr['vol_ltc']) * 100
        slot_opr_list = slot_opr.to_dict(orient='records')
        
        # Calculate Error Reasons (Sắp xếp theo tỷ trọng lỗi)
        reason_col = 'ly_do_tre_12h'
        df_late = df_opr[df_opr[reason_col] != '0.Ontime OPR']
        df_late = df_late.dropna(subset=[reason_col])
        
        # Late orders column
        if 'Đơn trễ' in df_late.columns:
            df_late['late_orders'] = df_late['Đơn trễ']
        else:
            df_late['late_orders'] = df_late['vol_ltc'] - df_late['ot']
            
        total_late = float(df_late['late_orders'].sum())
        
        errors = df_late.groupby(reason_col).agg({'late_orders': 'sum'}).reset_index()
        errors['weight'] = (errors['late_orders'] / total_late) * 100 if total_late > 0 else 0
        errors = errors.sort_values(by='late_orders', ascending=False)
        errors_list = errors.to_dict(orient='records')
        
        # Load OE_madh sheet (Detail N-1 error orders)
        if df_oe is None:
            df_oe = pd.read_excel(file_path, sheet_name="OE_madh")
        df_oe = df_oe.dropna(subset=["madh"]).copy()
        
        # Clean details
        df_oe = df_oe.where(pd.notnull(df_oe), None)
        oe_details = df_oe[['tutinh', 'kholay', 'sellername', 'khung_gio_tao_don', 'ly_do_tre_12h', 'madh', 'AM']].to_dict(orient='records')
        
        # Calculate OPR performance by AM
        am_opr = df_opr.groupby('AM').agg({'vol_ltc': 'sum', 'ot': 'sum'}).reset_index()
        am_opr['% OPR'] = (am_opr['ot'] / am_opr['vol_ltc']) * 100
        am_opr = am_opr.sort_values(by='% OPR', ascending=True).to_dict(orient='records')
        
        return {
            "overall_opr": overall_opr,
            "total_volume": int(total_vol),
            "total_ontime": int(total_ot),
            "total_late": int(total_late),
            "time_slots": slot_opr_list,
            "error_reasons": errors_list,
            "am_performance": am_opr,
            "oe_details": oe_details,
            "opr_n1": opr_n1,
            "opr_wk": opr_wk,
            "delta_n1": delta_n1,
            "delta_wk": delta_wk
        }
    except Exception as e:
        return {"error": f"Lỗi xử lý file OPR: {str(e)}"}

# ==========================================
# 3. PROCESS BACKLOG AGING
# ==========================================
def process_aging_backlog(df_raw=None, df_co_cau=None):
    file_path = os.path.join(WORKSPACE_DIR, 'Aging _5 ngày.xlsx')
    
    try:
        if df_raw is None or df_co_cau is None:
            if not os.path.exists(file_path):
                return {"error": f"Không tìm thấy file: {os.path.basename(file_path)}"}
            with pd.ExcelFile(file_path) as xls:
                if df_raw is None:
                    df_raw = pd.read_excel(xls, sheet_name="Đơn giao aging trên 5 ngày")
                if df_co_cau is None:
                    df_co_cau = pd.read_excel(xls, sheet_name="Cơ cấu")
                    
        df_raw = df_raw.dropna(subset=["Mã đơn"]).copy()
        df_co_cau = df_co_cau.dropna(subset=["Bưu cục"]).copy()
        
        df_raw = df_raw.dropna(subset=["Mã đơn"])
        df_co_cau = df_co_cau.dropna(subset=["Bưu cục"])
        
        # Map AM dynamically for rows where it is NaN
        # Clean warehouse strings for merge
        df_raw['bc_clean'] = df_raw['BC'].astype(str).str.strip().str.lower()
        df_co_cau['bc_clean'] = df_co_cau['Bưu cục'].astype(str).str.strip().str.lower()
        
        bc_to_am = dict(zip(df_co_cau['bc_clean'], df_co_cau['AM']))
        bc_to_province = dict(zip(df_co_cau['bc_clean'], df_co_cau['Tỉnh']))
        
        df_raw['mapped_am'] = df_raw['bc_clean'].map(bc_to_am)
        df_raw['mapped_province'] = df_raw['bc_clean'].map(bc_to_province)
        
        # Fallback to existing columns if map fails
        df_raw['final_am'] = df_raw['mapped_am'].fillna(df_raw['am_name']).fillna("Không xác định")
        df_raw['final_province'] = df_raw['mapped_province'].fillna(df_raw['Tỉnh']).fillna("Không xác định")
        
        # Categorize into aging brackets
        def get_aging_bracket(days):
            try:
                d = float(days)
                if d >= 5 and d < 8:
                    return "5 - 8 ngày"
                elif d >= 8 and d < 15:
                    return "8 - 15 ngày"
                elif d >= 15:
                    return "Trên 15 ngày"
            except:
                pass
            return "Khác"
            
        df_raw['aging_bracket'] = df_raw['Số ngày đã nhập BC'].apply(get_aging_bracket)
        df_raw = df_raw.where(pd.notnull(df_raw), None)
        
        # Summarize by AM and Bracket
        am_summary = df_raw.groupby(['final_am', 'aging_bracket']).size().unstack(fill_value=0).reset_index()
        # Ensure all columns exist
        for col in ["5 - 8 ngày", "8 - 15 ngày", "Trên 15 ngày"]:
            if col not in am_summary.columns:
                am_summary[col] = 0
        am_summary['Total'] = am_summary["5 - 8 ngày"] + am_summary["8 - 15 ngày"] + am_summary["Trên 15 ngày"]
        am_summary_list = am_summary.to_dict(orient='records')
        
        # Summarize by Post Office (BC)
        po_summary = df_raw.groupby(['BC', 'final_am', 'final_province', 'aging_bracket']).size().unstack(fill_value=0).reset_index()
        for col in ["5 - 8 ngày", "8 - 15 ngày", "Trên 15 ngày"]:
            if col not in po_summary.columns:
                po_summary[col] = 0
        po_summary['Total'] = po_summary["5 - 8 ngày"] + po_summary["8 - 15 ngày"] + po_summary["Trên 15 ngày"]
        po_summary_list = po_summary.to_dict(orient='records')
        
        # Raw records
        raw_records = df_raw[['final_province', 'BC', 'Mã đơn', 'Tệp khách', 'Số ngày đã nhập BC', 'Số lần giao', 'aging_bracket', 'final_am', 'Trạng thái']].to_dict(orient='records')
        
        return {
            "am_summary": am_summary_list,
            "po_summary": po_summary_list,
            "raw_records": raw_records,
            "total_backlog": len(df_raw)
        }
    except Exception as e:
        return {"error": f"Lỗi xử lý file aging backlog: {str(e)}"}

# ==========================================
# 4. PROCESS PENDING TRANSIT (TREO LUÂN CHUYỂN)
# ==========================================
def process_treo_backlog(df_raw=None, df_co_cau=None):
    file_path = os.path.join(WORKSPACE_DIR, 'Treo luân chuyển GIAO_TRẢ by IMTHIR.xlsx')
    
    try:
        if df_raw is None or df_co_cau is None:
            if not os.path.exists(file_path):
                return {"error": f"Không tìm thấy file: {os.path.basename(file_path)}"}
            with pd.ExcelFile(file_path) as xls:
                if df_raw is None:
                    df_raw = pd.read_excel(xls, sheet_name="stuck")
                if df_co_cau is None:
                    df_co_cau = pd.read_excel(xls, sheet_name="Cơ cấu")
                    
        df_raw = df_raw.dropna(subset=["Mã đơn hàng"]).copy()
        df_co_cau = df_co_cau.dropna(subset=["Bưu cục"]).copy()
        
        # Clean
        df_raw = df_raw.dropna(subset=["Mã đơn hàng"])
        df_co_cau = df_co_cau.dropna(subset=["Bưu cục"])
        
        # Apply filter: Trạng thái must be 'Chưa đóng kiện' or 'Không cần đóng kiện'
        allowed_statuses = ['Chưa đóng kiện', 'Không cần đóng kiện']
        df_raw = df_raw[df_raw['Trạng thái'].isin(allowed_statuses)]
        
        # Map AM dynamically via warehouse_name
        df_raw['wh_clean'] = df_raw['warehouse_name'].astype(str).str.strip().str.lower()
        df_co_cau['bc_clean'] = df_co_cau['Bưu cục'].astype(str).str.strip().str.lower()
        
        bc_to_am = dict(zip(df_co_cau['bc_clean'], df_co_cau['AM']))
        bc_to_province = dict(zip(df_co_cau['bc_clean'], df_co_cau['Tỉnh']))
        
        df_raw['mapped_am'] = df_raw['wh_clean'].map(bc_to_am)
        df_raw['mapped_province'] = df_raw['wh_clean'].map(bc_to_province)
        
        df_raw['final_am'] = df_raw['mapped_am'].fillna(df_raw['am_name']).fillna("Không xác định")
        df_raw['final_province'] = df_raw['mapped_province'].fillna(df_raw['province_name']).fillna("Không xác định")
        
        # Define delay brackets based on 'Thời gian tồn đọng'
        def get_treo_bracket(t):
            if not isinstance(t, str):
                return None
            t = t.strip()
            if t in ["36_48", "48_72"]:
                return "36 - 72h"
            elif t in ["72_96", "96_120"]:
                return "72 - 120h"
            elif t in ["120_192"]:
                return "120 - 192h"
            elif t in ["192", "192h+"]:
                return "192h+"
            return None

        df_raw['treo_bracket'] = df_raw['Thời gian tồn đọng'].apply(get_treo_bracket)
        df_raw = df_raw.dropna(subset=["treo_bracket"]) # Filter to delay > 36h
        
        df_raw = df_raw.where(pd.notnull(df_raw), None)
        
        # Split into Delivery (Giao) and Return (Trả)
        # Loại đơn has 'Luân chuyển giao' or 'Luân chuyển trả'
        df_giao = df_raw[df_raw['Loại đơn'] == 'Luân chuyển giao']
        df_tra = df_raw[df_raw['Loại đơn'] == 'Luân chuyển trả']
        
        # Helper to summarize df
        def get_summary_data(df_sub):
            if len(df_sub) == 0:
                return [], []
            
            # AM Summary
            am_sum = df_sub.groupby(['final_am', 'treo_bracket']).size().unstack(fill_value=0).reset_index()
            for col in ["36 - 72h", "72 - 120h", "120 - 192h", "192h+"]:
                if col not in am_sum.columns:
                    am_sum[col] = 0
            am_sum['Total'] = am_sum["36 - 72h"] + am_sum["72 - 120h"] + am_sum["120 - 192h"] + am_sum["192h+"]
            
            # PO Summary
            po_sum = df_sub.groupby(['warehouse_name', 'final_am', 'final_province', 'treo_bracket']).size().unstack(fill_value=0).reset_index()
            for col in ["36 - 72h", "72 - 120h", "120 - 192h", "192h+"]:
                if col not in po_sum.columns:
                    po_sum[col] = 0
            po_sum['Total'] = po_sum["36 - 72h"] + po_sum["72 - 120h"] + po_sum["120 - 192h"] + po_sum["192h+"]
            
            return am_sum.to_dict(orient='records'), po_sum.to_dict(orient='records')

        giao_am_sum, giao_po_sum = get_summary_data(df_giao)
        tra_am_sum, tra_po_sum = get_summary_data(df_tra)
        
        raw_records = df_raw[['final_province', 'warehouse_name', 'Mã đơn hàng', 'Loại đơn', 'Thời gian tồn đọng', 'treo_bracket', 'final_am', 'Trạng thái']].to_dict(orient='records')
        
        return {
            "giao_am_summary": giao_am_sum,
            "giao_po_summary": giao_po_sum,
            "tra_am_summary": tra_am_sum,
            "tra_po_summary": tra_po_sum,
            "raw_records": raw_records,
            "total_backlog": len(df_raw),
            "total_giao": len(df_giao),
            "total_tra": len(df_tra)
        }
    except Exception as e:
        return {"error": f"Lỗi xử lý file treo luân chuyển: {str(e)}"}

# ==========================================
# 4b. PROCESS UNSTABLE POST OFFICES
# ==========================================
def clean_po_name(name):
    if not name:
        return ""
    name = str(name).lower().strip()
    prefixes = ["bưu cục ", "kho giao hàng ", "kho giao ", "kho hàng ", "điểm xử lý ", "giao hàng nhanh ", "ghn "]
    for p in prefixes:
        if name.startswith(p):
            name = name[len(p):]
    replacements = {
        "khánh hoà": "khánh hòa",
        "đắc nông": "đắk nông",
        "bình phước": "lâm đồng",
        "-": " ",
        ".": " ",
        ",": " "
    }
    for k, v in replacements.items():
        name = name.replace(k, v)
    name = " ".join(name.split())
    return name

def map_po_to_am_prov(po_id, po_name, id_to_am, id_to_prov, name_to_am, name_to_prov, default_am="Không xác định", default_prov="Không xác định"):
    def clean_val(val, default):
        if pd.isna(val) or not str(val).strip() or str(val).lower() == 'nan':
            return default
        return str(val).strip()
    
    default_am = clean_val(default_am, "Không xác định")
    default_prov = clean_val(default_prov, "Không xác định")

    try:
        pid = int(float(po_id))
        if pid in id_to_am:
            return clean_val(id_to_am[pid], default_am), clean_val(id_to_prov[pid], default_prov)
    except:
        pass

    name_clean = clean_po_name(po_name)
    if name_clean in name_to_am:
        return clean_val(name_to_am[name_clean], default_am), clean_val(name_to_prov[name_clean], default_prov)

    for k in name_to_am:
        if k in name_clean or name_clean in k:
            return clean_val(name_to_am[k], default_am), clean_val(name_to_prov[k], default_prov)

    return default_am, default_prov

def process_unstable_po():
    file_path = os.path.join(WORKSPACE_DIR, 'buu_cuc_bat_on.xlsx')
    if not os.path.exists(file_path):
        return {"error": f"Không tìm thấy file: {os.path.basename(file_path)}. Vui lòng đồng bộ hoặc tải lên."}
    
    try:
        xls = pd.ExcelFile(file_path)
        sheet_name = None
        for s in xls.sheet_names:
            s_lower = s.lower()
            if "ntb" in s_lower or "bất ổn" in s_lower or "bat_on" in s_lower or "cảnh báo" in s_lower or "canh_bao" in s_lower:
                sheet_name = s
                break
        if not sheet_name:
            sheet_name = xls.sheet_names[0]
            
        df_raw = pd.read_excel(xls, sheet_name=sheet_name, header=None)
        
        update_time = None
        total_warning = None
        
        # Search metadata in the first 15 rows
        for r_idx in range(min(15, len(df_raw))):
            for c_idx in range(len(df_raw.columns)):
                cell_val = str(df_raw.iloc[r_idx, c_idx])
                if "Thời gian cập nhật" in cell_val:
                    for offset in range(1, 4):
                        if c_idx + offset < len(df_raw.columns):
                            val = df_raw.iloc[r_idx, c_idx + offset]
                            if pd.notna(val) and str(val).strip() != "":
                                update_time = str(val).strip()
                                break
                elif "bưu cục cảnh báo" in cell_val or "bưu cục bất ổn" in cell_val or "lượng bưu cục" in cell_val:
                    for offset in range(1, 4):
                        if c_idx + offset < len(df_raw.columns):
                            val = df_raw.iloc[r_idx, c_idx + offset]
                            if pd.notna(val) and str(val).strip() != "":
                                try:
                                    total_warning = int(float(val))
                                except:
                                    total_warning = str(val).strip()
                                break
        
        # Find the table headers row
        header_row_idx = None
        for r_idx in range(len(df_raw)):
            row_vals = [str(x).lower().strip() for x in df_raw.iloc[r_idx].values]
            if any("tổng số lượng" in x or "thời gian cập nhật" in x for x in row_vals):
                continue
            if any(x == "bưu cục" or x == "chi tiết" or x == "tên bc" or "tên bưu cục" in x or "kho_giao_id" in x or "kho_giao_name" in x or "tinh_giao" in x for x in row_vals):
                header_row_idx = r_idx
                break
                
        if header_row_idx is None:
            header_row_idx = 4 if len(df_raw) > 4 else 0
            
        # Load the table skipping rows before the header
        df_table = pd.read_excel(xls, sheet_name=sheet_name, skiprows=header_row_idx)
        df_table.columns = [str(c).strip() for c in df_table.columns]
        
        # Remove completely empty rows
        id_col = next((c for c in df_table.columns if "id" in c.lower() or "kho_giao_id" in c.lower()), df_table.columns[0])
        name_col = next((c for c in df_table.columns if "name" in c.lower() or "bưu cục" in c.lower() or "kho_giao_name" in c.lower()), df_table.columns[1] if len(df_table.columns) > 1 else df_table.columns[0])
        
        df_table = df_table.dropna(subset=[id_col, name_col], how='all')
        df_table = df_table[df_table[id_col].astype(str).str.strip() != ""]
        
        # Ensure we have clean mappings from co_cau_ntb.xlsx
        id_to_am = {}
        id_to_prov = {}
        name_to_am = {}
        name_to_prov = {}
        co_cau_path = os.path.join(WORKSPACE_DIR, 'co_cau_ntb.xlsx')
        if os.path.exists(co_cau_path):
            try:
                df_cc = pd.read_excel(co_cau_path, sheet_name='Sheet1')
                for _, r in df_cc.iterrows():
                    bc_id = r.get('warehouse_id')
                    bc_name = str(r.get('Bưu cục', '')).strip()
                    am = str(r.get('AM', '')).strip()
                    prov = str(r.get('Tỉnh', '')).strip()
                    if prov == 'Khánh Hoà':
                        prov = 'Khánh Hòa'
                    if prov == 'Bình Phước':
                        prov = 'Lâm Đồng'
                    
                    if pd.notna(bc_id):
                        try:
                            id_to_am[int(bc_id)] = am
                            id_to_prov[int(bc_id)] = prov
                        except:
                            pass
                    if bc_name:
                        name_clean = clean_po_name(bc_name)
                        name_to_am[name_clean] = am
                        name_to_prov[name_clean] = prov
            except Exception as e:
                print(f"Error reading co_cau_ntb.xlsx in process_unstable_po: {e}")

        # Now map each row in the df_table
        processed_records = []
        for _, r in df_table.iterrows():
            po_id = r.get(id_col)
            po_name = r.get(name_col)
            
            # Map AM/Prov
            mapped_am, mapped_prov = map_po_to_am_prov(po_id, po_name, id_to_am, id_to_prov, name_to_am, name_to_prov, r.get('AM', 'Không xác định'), r.get('tinh_giao', 'Không xác định'))
            
            # Map Column R: du_kien_clear_ton (18th column)
            days_col = next((c for c in df_table.columns if "du_kien_clear_ton" in c.lower() or "clear_ton" in c.lower() or c == "du_kien_clear_ton"), None)
            days_val = 0
            if days_col and days_col in df_table.columns:
                days_val = r[days_col]
            elif len(df_table.columns) > 17:
                days_val = r.iloc[17]
                
            try:
                days_val = int(float(days_val)) if pd.notna(days_val) else 0
            except:
                days_val = 0
                
            # Map Reason
            reason_col = next((c for c in df_table.columns if "ly_do" in c.lower() or "reason" in c.lower() or "ly_do_bat_on" in c.lower()), None)
            reason_val = ""
            if reason_col:
                reason_val = str(r[reason_col]).strip() if pd.notna(r[reason_col]) else ""
            elif len(df_table.columns) > 18:
                reason_val = str(r.iloc[18]).strip() if pd.notna(r.iloc[18]) else ""
                
            # Map Status
            status_col = next((c for c in df_table.columns if "trạng thái" in c.lower() or "status" in c.lower() or "trang_thai" in c.lower()), None)
            status_val = "Bình thường"
            if status_col:
                status_val = str(r[status_col]).strip() if pd.notna(r[status_col]) else "Bình thường"
            elif len(df_table.columns) > 19:
                status_val = str(r.iloc[19]).strip() if pd.notna(r.iloc[19]) else "Bình thường"
                
            record = {
                "id": int(float(po_id)) if pd.notna(po_id) else None,
                "name": str(po_name).strip() if pd.notna(po_name) else "",
                "am": mapped_am,
                "province": mapped_prov,
                "ton_lm": int(float(r.get('BL LM', 0))) if pd.notna(r.get('BL LM')) else 0,
                "ton_lm_5n": int(float(r.get('BL LM >5 ngay', 0))) if pd.notna(r.get('BL LM >5 ngay')) else 0,
                "pct_lm_5n": round(float(r.get('%BL LM >5 ngay', 0)) * 100, 2) if pd.notna(r.get('%BL LM >5 ngay')) else 0.0,
                "ton_ktc": int(float(r.get('BL KTC', 0))) if pd.notna(r.get('BL KTC')) else 0,
                "ton_ktc_cung_tinh": int(float(r.get('BL KTC cung tinh %', r.get('BL KTC cung tinh', 0)))) if pd.notna(r.get('BL KTC cung tinh %', r.get('BL KTC cung tinh'))) else 0,
                "pct_ktc_cung_tinh": round(float(r.get('%BL KTC cung tinh', 0)) * 100, 2) if pd.notna(r.get('%BL KTC cung tinh')) else 0.0,
                "days_unstable": days_val,
                "reason": reason_val,
                "status": status_val
            }
            processed_records.append(record)
            
        # Group warning/unstable post offices by AM (both Bất ổn and Chuẩn bị nhảy nhóm)
        unstable_by_am = {}
        for rec in processed_records:
            if rec["status"] in ["Bất ổn", "Chuẩn bị nhảy nhóm"]:
                am_name = rec["am"]
                if am_name not in unstable_by_am:
                    unstable_by_am[am_name] = []
                unstable_by_am[am_name].append(rec["name"])
                
        # Sort AMs by the number of warning post offices (descending)
        am_deepdive = []
        for am, pos in unstable_by_am.items():
            am_deepdive.append({
                "am": am,
                "count": len(pos),
                "pos": pos
            })
        am_deepdive = sorted(am_deepdive, key=lambda x: x["count"], reverse=True)
        
        # Calculate actual total warnings (both Bất ổn and Chuẩn bị nhảy nhóm)
        actual_total_warnings = sum(1 for rec in processed_records if rec["status"] in ["Bất ổn", "Chuẩn bị nhảy nhóm"])
        
        return {
            "update_time": update_time,
            "total_warning": actual_total_warnings,
            "records": clean_nan(processed_records),
            "am_deepdive": clean_nan(am_deepdive)
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": f"Lỗi xử lý bưu cục bất ổn: {str(e)}"}

def process_off_spe():
    file_path = os.path.join(WORKSPACE_DIR, 'off_tuyen_spe.xlsx')
    if not os.path.exists(file_path):
        return {"error": f"Không tìm thấy file: {os.path.basename(file_path)}. Vui lòng đồng bộ hoặc tải lên."}
    
    try:
        xls = pd.ExcelFile(file_path)
        sheet_name = None
        for s in xls.sheet_names:
            s_lower = s.lower()
            if "off" in s_lower:
                sheet_name = s
                break
        if not sheet_name:
            sheet_name = xls.sheet_names[0]
            
        df_raw = pd.read_excel(xls, sheet_name=sheet_name)
        
        # Remove empty rows or rows that have all NaN
        df_raw = df_raw.dropna(how='all')
        
        # Find columns dynamically
        col_tinh = next((c for c in df_raw.columns if "tỉnh" in c.lower() or "tinh" in c.lower() or "province" in c.lower()), None)
        col_quan = next((c for c in df_raw.columns if "quận" in c.lower() or "huyện" in c.lower() or "quan" in c.lower() or "huyen" in c.lower() or "district" in c.lower()), None)
        col_phuong = next((c for c in df_raw.columns if "phường" in c.lower() or "xã" in c.lower() or "phuong" in c.lower() or "xa" in c.lower() or "ward" in c.lower()), None)
        col_bc = next((c for c in df_raw.columns if "bưu cục" in c.lower() or "buu cuc" in c.lower() or "post" in c.lower() or "bc" in c.lower()), None)
        col_ketqua = next((c for c in df_raw.columns if "kết quả" in c.lower() or "ket qua" in c.lower() or "update" in c.lower()), None)
        col_capdown = next((c for c in df_raw.columns if "cap" in c.lower() or "down" in c.lower() or "%" in c.lower()), None)
        col_time_off = next((c for c in df_raw.columns if "thời gian tắt" in c.lower() or "thoi gian tat" in c.lower() or "tg tắt" in c.lower() or "tg tat" in c.lower()), None)
        col_time_on = next((c for c in df_raw.columns if "thời gian mở" in c.lower() or "thoi gian mo" in c.lower() or "tg mở" in c.lower() or "tg mo" in c.lower()), None)
        col_note = next((c for c in df_raw.columns if "note" in c.lower() or "ghi chú" in c.lower() or "ghi chu" in c.lower()), None)
        
        # Fallback to indices if columns not found dynamically
        cols = list(df_raw.columns)
        if not col_tinh and len(cols) > 0: col_tinh = cols[0]
        if not col_quan and len(cols) > 1: col_quan = cols[1]
        if not col_phuong and len(cols) > 2: col_phuong = cols[2]
        if not col_bc and len(cols) > 3: col_bc = cols[3]
        if not col_ketqua and len(cols) > 4: col_ketqua = cols[4]
        if not col_capdown and len(cols) > 5: col_capdown = cols[5]
        if not col_time_off and len(cols) > 6: col_time_off = cols[6]
        if not col_time_on and len(cols) > 7: col_time_on = cols[7]
        if not col_note and len(cols) > 8: col_note = cols[8]
        
        df_table = df_raw.dropna(subset=[col_tinh, col_bc], how='all')
        
        processed_records = []
        total_off = 0
        total_pending = 0
        
        # Map standard dates if they look like timestamp objects
        def clean_date_str(val):
            if pd.isna(val):
                return ""
            if isinstance(val, (datetime.datetime, pd.Timestamp)):
                return val.strftime("%d-%m-%Y")
            val_str = str(val).strip()
            # If timestamp string, format it
            if "00:00:00" in val_str:
                val_str = val_str.replace(" 00:00:00", "")
            return val_str
            
        for _, r in df_table.iterrows():
            tinh_val = str(r[col_tinh]).strip() if col_tinh and pd.notna(r[col_tinh]) else "Không xác định"
            quan_val = str(r[col_quan]).strip() if col_quan and pd.notna(r[col_quan]) else ""
            phuong_val = str(r[col_phuong]).strip() if col_phuong and pd.notna(r[col_phuong]) else ""
            bc_val = str(r[col_bc]).strip() if col_bc and pd.notna(r[col_bc]) else ""
            
            # Status:
            # - Column E has "duyệt" => Đang OFF
            # - Column E empty => Đang chờ duyệt
            kq_raw = r[col_ketqua] if col_ketqua else ""
            kq_val = str(kq_raw).strip().lower() if pd.notna(kq_raw) else ""
            
            if pd.isna(kq_raw) or not kq_val:
                status_val = "Đang chờ duyệt"
                total_pending += 1
            elif "duyệt" in kq_val:
                status_val = "Đang OFF"
                total_off += 1
            else:
                status_val = "Đang chờ duyệt"
                total_pending += 1
                
            capdown_val = ""
            if col_capdown and pd.notna(r[col_capdown]):
                try:
                    val_float = float(r[col_capdown])
                    if val_float <= 1.0:
                        capdown_val = f"{int(val_float * 100)}%"
                    else:
                        capdown_val = f"{int(val_float)}%"
                except:
                    capdown_val = str(r[col_capdown]).strip()
                    
            time_off_val = clean_date_str(r[col_time_off]) if col_time_off else ""
            time_on_val = clean_date_str(r[col_time_on]) if col_time_on else ""
            note_val = str(r[col_note]).strip() if col_note and pd.notna(r[col_note]) else ""
            
            processed_records.append({
                "province": tinh_val,
                "district": quan_val,
                "ward": phuong_val,
                "post_office": bc_val,
                "status": status_val,
                "pct_cap_down": capdown_val,
                "off_time": time_off_val,
                "on_time": time_on_val,
                "note": note_val
            })
            
        mtime = os.path.getmtime(file_path)
        update_time = datetime.datetime.fromtimestamp(mtime).strftime("%d-%m-%Y %H:%M:%S")
        
        return {
            "update_time": update_time,
            "total_off": total_off,
            "total_pending": total_pending,
            "records": clean_nan(processed_records)
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": f"Lỗi xử lý file off_tuyen_spe.xlsx: {str(e)}"}

# ==========================================
# 5. SYNC & HISTORY CACHE MANAGEMENT
# ==========================================
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_history(history):
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving history: {e}")

# Save current run to history
def add_to_history(aging_data, treo_data):
    history = load_history()
    
    # Format date and time
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save simple metrics map for comparison
    aging_am_map = {}
    for r in aging_data.get("am_summary", []):
        aging_am_map[r["final_am"]] = int(r["Total"])
        
    aging_po_map = {}
    for r in aging_data.get("po_summary", []):
        aging_po_map[r["BC"]] = int(r["Total"])
        
    treo_giao_am_map = {}
    for r in treo_data.get("giao_am_summary", []):
        treo_giao_am_map[r["final_am"]] = int(r["Total"])
        
    treo_giao_po_map = {}
    for r in treo_data.get("giao_po_summary", []):
        treo_giao_po_map[r["warehouse_name"]] = int(r["Total"])
        
    treo_tra_am_map = {}
    for r in treo_data.get("tra_am_summary", []):
        treo_tra_am_map[r["final_am"]] = int(r["Total"])
        
    treo_tra_po_map = {}
    for r in treo_data.get("tra_po_summary", []):
        treo_tra_po_map[r["warehouse_name"]] = int(r["Total"])
        
    new_entry = {
        "timestamp": now_str,
        "aging_total": aging_data.get("total_backlog", 0),
        "treo_total": treo_data.get("total_backlog", 0),
        "treo_giao_total": treo_data.get("total_giao", 0),
        "treo_tra_total": treo_data.get("total_tra", 0),
        "aging_am_map": aging_am_map,
        "aging_po_map": aging_po_map,
        "treo_giao_am_map": treo_giao_am_map,
        "treo_giao_po_map": treo_giao_po_map,
        "treo_tra_am_map": treo_tra_am_map,
        "treo_tra_po_map": treo_tra_po_map
    }
    
    history.append(new_entry)
    # Keep last 20 entries
    if len(history) > 20:
        history = history[-20:]
    save_history(history)
    return now_str

# Helper to calculate chênh lệch (+/-) based on history entry
def calculate_trend(current_data, baseline_entry):
    if not baseline_entry:
        return current_data
        
    # Process Aging Backlog
    aging_am_map = baseline_entry.get("aging_am_map", {})
    aging_po_map = baseline_entry.get("aging_po_map", {})
    
    for r in current_data["aging"].get("am_summary", []):
        prev = aging_am_map.get(r["final_am"], 0)
        r["diff"] = int(r["Total"]) - prev
        
    for r in current_data["aging"].get("po_summary", []):
        prev = aging_po_map.get(r["BC"], 0)
        r["diff"] = int(r["Total"]) - prev
        
    current_data["aging"]["diff_total"] = current_data["aging"].get("total_backlog", 0) - baseline_entry.get("aging_total", 0)
    
    # Process Treo luân chuyển
    tg_am_map = baseline_entry.get("treo_giao_am_map", {})
    tg_po_map = baseline_entry.get("treo_giao_po_map", {})
    tt_am_map = baseline_entry.get("treo_tra_am_map", {})
    tt_po_map = baseline_entry.get("treo_tra_po_map", {})
    
    for r in current_data["treo"].get("giao_am_summary", []):
        prev = tg_am_map.get(r["final_am"], 0)
        r["diff"] = int(r["Total"]) - prev
        
    for r in current_data["treo"].get("giao_po_summary", []):
        prev = tg_po_map.get(r["warehouse_name"], 0)
        r["diff"] = int(r["Total"]) - prev
        
    for r in current_data["treo"].get("tra_am_summary", []):
        prev = tt_am_map.get(r["final_am"], 0)
        r["diff"] = int(r["Total"]) - prev
        
    for r in current_data["treo"].get("tra_po_summary", []):
        prev = tt_po_map.get(r["warehouse_name"], 0)
        r["diff"] = int(r["Total"]) - prev
        
    current_data["treo"]["diff_total"] = current_data["treo"].get("total_backlog", 0) - baseline_entry.get("treo_total", 0)
    current_data["treo"]["diff_giao"] = current_data["treo"].get("total_giao", 0) - baseline_entry.get("treo_giao_total", 0)
    current_data["treo"]["diff_tra"] = current_data["treo"].get("total_tra", 0) - baseline_entry.get("treo_tra_total", 0)
    
    return current_data

# ==========================================
# 6. IN-MEMORY CACHE DECLARATION & INITIALIZATION
# ==========================================
OPERATIONAL_CACHE = None
OPR_CACHE = None
BACKLOG_CACHE_RAW = None
UNSTABLE_PO_CACHE = None
OFF_SPE_CACHE = None

# Dataframe caches for NTB Summary Dashboard
DF_GTC_CACHE = None
DF_LTC_CACHE = None
DF_CO_CAU_CACHE = None
DF_AGING_CACHE = None
DF_TREO_CACHE = None
DF_TAO_DON_CACHE = None
DF_BUU_CUC_TYPE_MAP = None

def load_buu_cuc_type_map():
    file_path = os.path.join(WORKSPACE_DIR, 'buu_cuc_bat_on.xlsx')
    if not os.path.exists(file_path):
        return {}
    try:
        xls = pd.ExcelFile(file_path)
        sheet_name = None
        for s in xls.sheet_names:
            s_lower = s.lower()
            if "ntb" in s_lower or "bất ổn" in s_lower or "bat_on" in s_lower or "cảnh báo" in s_lower or "canh_bao" in s_lower:
                sheet_name = s
                break
        if not sheet_name:
            sheet_name = xls.sheet_names[0]
        df_raw = pd.read_excel(xls, sheet_name=sheet_name, header=None)
        header_row_idx = None
        for r_idx in range(len(df_raw)):
            row_vals = [str(x).lower().strip() for x in df_raw.iloc[r_idx].values]
            if any("tổng số lượng" in x or "thời gian cập nhật" in x for x in row_vals):
                continue
            if any(x == "bưu cục" or x == "chi tiết" or x == "tên bc" or "tên bưu cục" in x or "kho_giao_id" in x or "kho_giao_name" in x or "tinh_giao" in x for x in row_vals):
                header_row_idx = r_idx
                break
        if header_row_idx is None:
            header_row_idx = 4 if len(df_raw) > 4 else 0
        df_table = pd.read_excel(xls, sheet_name=sheet_name, skiprows=header_row_idx)
        df_table.columns = [str(c).strip() for c in df_table.columns]
        
        id_col = next((c for c in df_table.columns if "id" in c.lower() or "kho_giao_id" in c.lower()), None)
        type_col = next((c for c in df_table.columns if "type" in c.lower() or "warehouse_type" in c.lower() or "loại" in c.lower()), None)
        
        if id_col and type_col:
            df_table = df_table.dropna(subset=[id_col, type_col])
            type_map = {}
            for _, row in df_table.iterrows():
                try:
                    p_id = int(float(row[id_col]))
                    p_type = str(row[type_col]).strip()
                    type_map[p_id] = p_type
                except:
                    pass
            return type_map
    except Exception as e:
        print(f"Error loading buu_cuc_type_map: {e}")
    return {}

def load_vols_tao_don_df():
    file_path = os.path.join(WORKSPACE_DIR, 'vols_tao_don.xlsx')
    if not os.path.exists(file_path):
        return None
    try:
        xls = pd.ExcelFile(file_path)
        sheet_name = "shopee_tiktok" if "shopee_tiktok" in xls.sheet_names else xls.sheet_names[0]
        df = pd.read_excel(xls, sheet_name=sheet_name)
        df.columns = [str(c).strip() for c in df.columns]
        df['Date'] = pd.to_datetime(df['Date'])
        df = df[df['bat_on'].fillna('').str.strip() != 'BC Cũ/Không thuộc ĐCL'].copy()
        return df
    except Exception as e:
        print(f"Error loading vols_tao_don.xlsx: {e}")
    return None

def clean_str_key(val):
    if pd.isna(val):
        return "unknown"
    val = str(val).strip().lower()
    replacements = {
        "lâm đồng": "lam_dong",
        "bình thuận": "binh_thuan",
        "khánh hòa": "khanh_hoa",
        "ninh thuận": "ninh_thuan",
        "đắk nông": "dak_nong",
        "đắc nông": "dak_nong"
    }
    return replacements.get(val, val.replace(" ", "_"))

@with_lock(CACHE_LOCK)
def get_dataframes(force=False, raw_gtc=None, raw_ltc=None, raw_co_cau=None, raw_aging=None, raw_co_cau_aging=None, raw_treo=None, raw_co_cau_treo=None):
    global DF_GTC_CACHE, DF_LTC_CACHE, DF_CO_CAU_CACHE, DF_AGING_CACHE, DF_TREO_CACHE
    if force or DF_GTC_CACHE is None or DF_LTC_CACHE is None or DF_CO_CAU_CACHE is None or DF_AGING_CACHE is None or DF_TREO_CACHE is None:
        file_path = os.path.join(WORKSPACE_DIR, 'Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx')
        
        if raw_gtc is None or raw_ltc is None or raw_co_cau is None:
            if not os.path.exists(file_path):
                raise FileNotFoundError("Không tìm thấy file: BÁO CÁO VẬN HÀNH")
            with pd.ExcelFile(file_path) as xls:
                if raw_gtc is None:
                    raw_gtc = read_ops_sheet(xls, "gtc")
                if raw_ltc is None:
                    raw_ltc = read_ops_sheet(xls, "ltc")
                if raw_co_cau is None:
                    raw_co_cau = read_ops_sheet(xls, "co_cau")
        
        df_gtc = raw_gtc[raw_gtc['Cấp Quản Lý'] != 'Grand Total'].dropna(subset=["Volume"]).copy()
        df_gtc['Leadtime'] = pd.to_numeric(df_gtc['Leadtime'], errors='coerce')
        
        df_ltc = raw_ltc[raw_ltc['Cấp quản lý'] != 'Grand Total'].dropna(subset=["Volume"]).copy()
        df_ltc['Leadtime'] = pd.to_numeric(df_ltc['Leadtime'], errors='coerce')
        
        df_co_cau = raw_co_cau.copy()
        
        path_aging = os.path.join(WORKSPACE_DIR, 'Aging _5 ngày.xlsx')
        if raw_aging is None or raw_co_cau_aging is None:
            if not os.path.exists(path_aging):
                raise FileNotFoundError("Không tìm thấy file: Aging _5 ngày")
            with pd.ExcelFile(path_aging) as xls:
                if raw_aging is None:
                    raw_aging = pd.read_excel(xls, sheet_name="Đơn giao aging trên 5 ngày")
                if raw_co_cau_aging is None:
                    raw_co_cau_aging = pd.read_excel(xls, sheet_name="Cơ cấu")
                    
        df_aging = raw_aging.copy()
        df_co_cau_aging = raw_co_cau_aging.copy()
        
        path_treo = os.path.join(WORKSPACE_DIR, 'Treo luân chuyển GIAO_TRẢ by IMTHIR.xlsx')
        if raw_treo is None or raw_co_cau_treo is None:
            if not os.path.exists(path_treo):
                raise FileNotFoundError("Không tìm thấy file: Treo luân chuyển")
            with pd.ExcelFile(path_treo) as xls:
                if raw_treo is None:
                    raw_treo = pd.read_excel(xls, sheet_name="stuck")
                if raw_co_cau_treo is None:
                    raw_co_cau_treo = pd.read_excel(xls, sheet_name="Cơ cấu")
                    
        df_treo = raw_treo.copy()
        df_co_cau_treo = raw_co_cau_treo.copy()
        
        bc_to_am = {}
        bc_to_prov = {}
        
        for df_cc in [df_co_cau, df_co_cau_aging, df_co_cau_treo]:
            for _, r in df_cc.iterrows():
                bc = str(r.get('BC', '')).strip().lower()
                buucuc = str(r.get('Bưu cục', '')).strip().lower()
                am = str(r.get('Am', r.get('ID - Họ Tên Am', ''))).strip()
                prov = str(r.get('Tỉnh', '')).strip()
                if prov == 'Bình Phước':
                    prov = 'Lâm Đồng'
                if bc and bc != 'nan':
                    bc_to_am[bc] = am
                    bc_to_prov[bc] = prov
                if buucuc and buucuc != 'nan':
                    bc_to_am[buucuc] = am
                    bc_to_prov[buucuc] = prov
                    
        df_gtc['clean_bc'] = df_gtc['Chi tiết'].apply(clean_str)
        df_gtc['mapped_prov'] = df_gtc['clean_bc'].map(bc_to_prov).fillna(df_gtc['Tỉnh']).fillna("Không xác định")
        df_gtc['mapped_am'] = df_gtc['clean_bc'].map(bc_to_am).fillna(df_gtc['AM']).fillna("Không xác định")
        df_gtc['delivered_vol'] = df_gtc['Volume'] * df_gtc['% GTC']
        df_gtc['return_vol'] = df_gtc['Volume'] * df_gtc['% Chuyển trả']
        df_gtc['ttc_vol'] = df_gtc['delivered_vol'] + df_gtc['return_vol']
        
        df_ltc['clean_bc'] = df_ltc['Chi tiết'].apply(clean_str)
        prov_col = next((c for c in df_ltc.columns if c.lower() == 'tỉnh'), None)
        am_col = next((c for c in df_ltc.columns if c.lower() == 'am'), None)
        
        df_ltc['mapped_prov'] = df_ltc['clean_bc'].map(bc_to_prov)
        if prov_col:
            df_ltc['mapped_prov'] = df_ltc['mapped_prov'].fillna(df_ltc[prov_col])
        df_ltc['mapped_prov'] = df_ltc['mapped_prov'].fillna("Không xác định")
        
        df_ltc['mapped_am'] = df_ltc['clean_bc'].map(bc_to_am)
        if am_col:
            df_ltc['mapped_am'] = df_ltc['mapped_am'].fillna(df_ltc[am_col])
        df_ltc['mapped_am'] = df_ltc['mapped_am'].fillna("Không xác định")
        df_ltc['ltc_vol'] = df_ltc['Volume'] * df_ltc['%LTC']
        
        df_aging['clean_bc'] = df_aging['BC'].apply(clean_str)
        df_aging['mapped_prov'] = df_aging['clean_bc'].map(bc_to_prov).fillna(df_aging['Tỉnh']).fillna("Không xác định")
        df_aging['mapped_am'] = df_aging['clean_bc'].map(bc_to_am).fillna(df_aging['am_name']).fillna("Không xác định")
        
        df_treo['clean_bc'] = df_treo['warehouse_name'].apply(clean_str)
        df_treo['mapped_prov'] = df_treo['clean_bc'].map(bc_to_prov).fillna(df_treo['province_name']).fillna("Không xác định")
        df_treo['mapped_am'] = df_treo['clean_bc'].map(bc_to_am).fillna(df_treo['am_name']).fillna("Không xác định")
        
        allowed_statuses = ['Chưa đóng kiện', 'Không cần đóng kiện']
        df_treo_filtered = df_treo[df_treo['Trạng thái'].isin(allowed_statuses)].copy()
        
        def get_treo_bracket_local(t):
            if not isinstance(t, str):
                return None
            t = t.strip()
            if t in ["36_48", "48_72"]:
                return "36 - 72h"
            elif t in ["72_96", "96_120"]:
                return "72 - 120h"
            elif t in ["120_192"]:
                return "120 - 192h"
            elif t in ["192", "192h+"]:
                return "192h+"
            return None

        df_treo_filtered['treo_bracket'] = df_treo_filtered['Thời gian tồn đọng'].apply(get_treo_bracket_local)
        df_treo_filtered = df_treo_filtered.dropna(subset=["treo_bracket"])
        
        DF_GTC_CACHE = df_gtc
        DF_LTC_CACHE = df_ltc
        DF_CO_CAU_CACHE = df_co_cau
        DF_AGING_CACHE = df_aging
        DF_TREO_CACHE = df_treo_filtered
        
    return DF_GTC_CACHE, DF_LTC_CACHE, DF_AGING_CACHE, DF_TREO_CACHE

def apply_filters(df, am=None, province=None, post_office=None):
    df_filtered = df.copy()
    if am:
        df_filtered = df_filtered[df_filtered['mapped_am'] == am]
    if province:
        df_filtered = df_filtered[df_filtered['mapped_prov'] == province]
    if post_office:
        df_filtered = df_filtered[df_filtered['clean_bc'] == post_office.strip().lower()]
    return df_filtered

@with_lock(CACHE_LOCK)
def update_all_caches():
    global OPERATIONAL_CACHE, OPR_CACHE, BACKLOG_CACHE_RAW, UNSTABLE_PO_CACHE, OFF_SPE_CACHE, DF_TAO_DON_CACHE, DF_BUU_CUC_TYPE_MAP
    print("--------------------------------------------------")
    print("STARTING CACHE LOAD: Processing raw Excel files...")
    print("--------------------------------------------------")
    
    try:
        # Load all files once in one go
        path_ops = os.path.join(WORKSPACE_DIR, 'Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx')
        print("Loading Copy o NTB - BAO CAO VAN HANH.xlsx...")
        with pd.ExcelFile(path_ops) as xls_ops:
            raw_gtc = read_ops_sheet(xls_ops, "gtc")
            raw_ltc = read_ops_sheet(xls_ops, "ltc")
            raw_co_cau = read_ops_sheet(xls_ops, "co_cau")
            
        path_aging = os.path.join(WORKSPACE_DIR, 'Aging _5 ngày.xlsx')
        print("Loading Aging _5 ngay.xlsx...")
        with pd.ExcelFile(path_aging) as xls_aging:
            raw_aging = pd.read_excel(xls_aging, sheet_name="Đơn giao aging trên 5 ngày")
            raw_co_cau_aging = pd.read_excel(xls_aging, sheet_name="Cơ cấu")
            
        path_treo = os.path.join(WORKSPACE_DIR, 'Treo luân chuyển GIAO_TRẢ by IMTHIR.xlsx')
        print("Loading Treo luan chuyen GIAO_TRA by IMTHIR.xlsx...")
        with pd.ExcelFile(path_treo) as xls_treo:
            raw_treo = pd.read_excel(xls_treo, sheet_name="stuck")
            raw_co_cau_treo = pd.read_excel(xls_treo, sheet_name="Cơ cấu")
            
        path_opr = os.path.join(WORKSPACE_DIR, 'OPR TTS.xlsx')
        print("Loading OPR TTS.xlsx...")
        with pd.ExcelFile(path_opr) as xls_opr:
            raw_opr = pd.read_excel(xls_opr, sheet_name="OPR")
            raw_oe = pd.read_excel(xls_opr, sheet_name="OE_madh")
            raw_rawopr = pd.read_excel(xls_opr, sheet_name="rawopr") if "rawopr" in xls_opr.sheet_names else None
            
    except Exception as e:
        err_msg = f"Loi doc file Excel: {str(e)}"
        print(err_msg.encode('ascii', errors='backslashreplace').decode('ascii'))
        OPERATIONAL_CACHE = {"error": err_msg}
        OPR_CACHE = {"error": err_msg}
        BACKLOG_CACHE_RAW = {"aging": {"error": err_msg}, "treo": {"error": err_msg}}
        UNSTABLE_PO_CACHE = {"error": err_msg}
        OFF_SPE_CACHE = {"error": err_msg}
        return
        
    # Preload dataframes
    print("Preloading pandas dataframes for NTB summary dashboard...")
    try:
        get_dataframes(force=True,
                       raw_gtc=raw_gtc, raw_ltc=raw_ltc, raw_co_cau=raw_co_cau,
                       raw_aging=raw_aging, raw_co_cau_aging=raw_co_cau_aging,
                       raw_treo=raw_treo, raw_co_cau_treo=raw_co_cau_treo)
        print("-> Dataframes loaded and cached successfully.")
    except Exception as e:
        print(f"-> Error preloading dataframes: {str(e)}")
        
    # 1. Operational Report
    print("Parsing 'Copy o NTB - BAO CAO VAN HANH.xlsx'...")
    ops = process_operational_report(df_gtc=raw_gtc, df_ltc=raw_ltc)
    if "error" not in ops:
        OPERATIONAL_CACHE = ops
        print("-> Operational report loaded and cached successfully.")
    else:
        OPERATIONAL_CACHE = ops  # Store error dictionary
        print("-> Error parsing operational report.")
        
    # 2. OPR Report
    print("Parsing 'OPR TTS.xlsx'...")
    opr = process_opr_report(df_opr=raw_opr, df_oe=raw_oe, df_rawopr=raw_rawopr)
    if "error" not in opr:
        OPR_CACHE = opr
        print("-> OPR report loaded and cached successfully.")
    else:
        OPR_CACHE = opr  # Store error dictionary
        print("-> Error parsing OPR report.")
        
    # 3. Backlog Reports (Aging + Treo)
    print("Parsing 'Aging _5 ngay.xlsx' and 'Treo luan chuyen GIAO_TRA by IMTHIR.xlsx'...")
    aging = process_aging_backlog(df_raw=raw_aging, df_co_cau=raw_co_cau_aging)
    treo = process_treo_backlog(df_raw=raw_treo, df_co_cau=raw_co_cau_treo)
    BACKLOG_CACHE_RAW = {
        "aging": aging,
        "treo": treo
    }
    if "error" not in aging and "error" not in treo:
        print("-> Backlog reports loaded and cached successfully.")
    else:
        print("-> Error parsing backlog reports.")
        
    # 4. Unstable Post Offices
    print("Parsing 'buu_cuc_bat_on.xlsx'...")
    UNSTABLE_PO_CACHE = process_unstable_po()
    if "error" not in UNSTABLE_PO_CACHE:
        print("-> Unstable PO cache loaded successfully.")
    else:
        print(f"-> Unstable PO status: {UNSTABLE_PO_CACHE['error']}")
        
    # 5. OFF SPE Routes
    print("Parsing 'off_tuyen_spe.xlsx'...")
    OFF_SPE_CACHE = process_off_spe()
    if "error" not in OFF_SPE_CACHE:
        print("-> OFF SPE cache loaded successfully.")
    else:
        print(f"-> OFF SPE status: {OFF_SPE_CACHE['error']}")
        
    # 6. Volume Creation Data
    print("Parsing 'vols_tao_don.xlsx' and warehouse type mapping...")
    DF_TAO_DON_CACHE = load_vols_tao_don_df()
    DF_BUU_CUC_TYPE_MAP = load_buu_cuc_type_map()
    if DF_TAO_DON_CACHE is not None:
        print("-> Volume creation cache loaded successfully.")
    else:
        print("-> Volume creation cache failed or is empty.")
        
    print("--------------------------------------------------")
    print("CACHE LOAD COMPLETE.")
    print("--------------------------------------------------")

# ==========================================
# 7. API FLASK ENDPOINTS
# ==========================================
@app.route('/')
@requires_auth
def home():
    return render_template('index.html')

@app.route('/api/unstable-po')
@requires_auth
def get_unstable_po():
    global UNSTABLE_PO_CACHE
    if UNSTABLE_PO_CACHE is None:
        with CACHE_LOCK:
            if UNSTABLE_PO_CACHE is None:
                UNSTABLE_PO_CACHE = process_unstable_po()
    return jsonify(UNSTABLE_PO_CACHE)

@app.route('/api/off-spe')
@requires_auth
def get_off_spe():
    global OFF_SPE_CACHE
    if OFF_SPE_CACHE is None:
        with CACHE_LOCK:
            if OFF_SPE_CACHE is None:
                OFF_SPE_CACHE = process_off_spe()
    return jsonify(OFF_SPE_CACHE)

@app.route('/api/operational')
@requires_auth
def get_operational():
    global OPERATIONAL_CACHE
    with CACHE_LOCK:
        if OPERATIONAL_CACHE is None:
            OPERATIONAL_CACHE = process_operational_report()
    return jsonify(clean_nan(OPERATIONAL_CACHE))

@app.route('/api/opr')
@requires_auth
def get_opr():
    global OPR_CACHE
    with CACHE_LOCK:
        if OPR_CACHE is None:
            OPR_CACHE = process_opr_report()
    return jsonify(clean_nan(OPR_CACHE))

@app.route('/api/backlog')
@requires_auth
def get_backlog():
    global BACKLOG_CACHE_RAW
    with CACHE_LOCK:
        if BACKLOG_CACHE_RAW is None:
            aging = process_aging_backlog()
            treo = process_treo_backlog()
            BACKLOG_CACHE_RAW = {
                "aging": aging,
                "treo": treo
            }
        
    if "error" in BACKLOG_CACHE_RAW["aging"]:
        return jsonify({"error": BACKLOG_CACHE_RAW["aging"]["error"]})
    if "error" in BACKLOG_CACHE_RAW["treo"]:
        return jsonify({"error": BACKLOG_CACHE_RAW["treo"]["error"]})
        
    history = load_history()
    baseline_ts = request.args.get("baseline")
    baseline_entry = None
    
    if history:
        if baseline_ts:
            for entry in history:
                if entry["timestamp"] == baseline_ts:
                    baseline_entry = entry
                    break
        else:
            if len(history) >= 2:
                baseline_entry = history[-2]
            else:
                baseline_entry = history[-1]
                
    import copy
    current_data = copy.deepcopy(BACKLOG_CACHE_RAW)
    current_data["baseline_timestamp"] = baseline_entry["timestamp"] if baseline_entry else None
    current_data = calculate_trend(current_data, baseline_entry)
    
    return jsonify(clean_nan(current_data))

@app.route('/api/history')
@requires_auth
def get_history():
    history = load_history()
    timestamps = [entry["timestamp"] for entry in history]
    return jsonify(timestamps[::-1])

@app.route('/api/user-role')
@requires_auth
def get_user_role():
    role = 'admin' if is_admin() else 'staff'
    return jsonify({"username": request.authorization.username, "role": role})

def mask_url(url):
    if not url:
        return ""
    match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
    if not match:
        return url
    spreadsheet_id = match.group(1)
    if len(spreadsheet_id) > 10:
        masked_id = spreadsheet_id[:4] + "****************" + spreadsheet_id[-4:]
    else:
        masked_id = "********"
    masked_url = url.replace(spreadsheet_id, masked_id)
    return masked_url

@app.route('/api/config', methods=['GET', 'POST'])
@requires_auth
def manage_config():
    if request.method == 'POST':
        if not is_admin():
            return jsonify({"error": "Quyền truy cập bị từ chối. Chỉ tài khoản admin mới được phép lưu cấu hình."}), 403
        try:
            data = request.json or {}
            current_config = load_config()
            
            config = {}
            for k in ["ops_url", "opr_url", "aging_url", "treo_url", "bat_on_url", "off_spe_url", "tao_don_url"]:
                val = data.get(k, "").strip()
                if not val:
                    config[k] = ""
                elif "*" in val or "Ẩn" in val or "hidden" in val.lower():
                    config[k] = current_config.get(k, "")
                else:
                    if not (val.startswith("https://docs.google.com/spreadsheets/") or val.startswith("http://docs.google.com/spreadsheets/")):
                        return jsonify({"error": f"Link Google Sheet không hợp lệ cho {k}. Phải bắt đầu bằng https://docs.google.com/spreadsheets/"}), 400
                    config[k] = val
            
            if save_config(config):
                masked_config = {k: mask_url(v) for k, v in config.items()}
                return jsonify({"success": True, "config": masked_config})
            else:
                return jsonify({"error": "Không thể ghi cấu hình."}), 500
        except Exception as e:
            return jsonify({"error": f"Lỗi xử lý yêu cầu: {str(e)}"}), 400
    else:
        config = load_config()
        masked_config = {k: mask_url(v) for k, v in config.items()}
        return jsonify(masked_config)

@app.route('/api/download-template', methods=['GET'])
@requires_auth
def download_template():
    from flask import send_from_directory
    filename = request.args.get('filename', '').strip()
    allowed_files = [
        'Aging _5 ngày.xlsx',
        'Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx',
        'OPR TTS.xlsx',
        'Treo luân chuyển GIAO_TRẢ by IMTHIR.xlsx',
        'buu_cuc_bat_on.xlsx',
        'off_tuyen_spe.xlsx',
        'vols_tao_don.xlsx'
    ]
    if filename not in allowed_files:
        return jsonify({"error": "Tên file không hợp lệ."}), 400
        
    try:
        return send_from_directory(WORKSPACE_DIR, filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": f"Không thể tải file: {str(e)}"}), 500

@app.route('/api/upload', methods=['POST'])
@requires_auth
def upload_file():
    global OPERATIONAL_CACHE, OPR_CACHE, BACKLOG_CACHE_RAW
    if 'file' not in request.files:
        return jsonify({"error": "Không tìm thấy file trong yêu cầu."}), 400
        
    file = request.files['file']
    filename = request.form.get('filename', '').strip()
    
    if not filename:
        return jsonify({"error": "Không xác định được tên file đích."}), 400
        
    allowed_files = [
        'Aging _5 ngày.xlsx',
        'Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx',
        'OPR TTS.xlsx',
        'Treo luân chuyển GIAO_TRẢ by IMTHIR.xlsx',
        'buu_cuc_bat_on.xlsx',
        'off_tuyen_spe.xlsx',
        'vols_tao_don.xlsx'
    ]
    
    if filename not in allowed_files:
        return jsonify({"error": "Tên file không hợp lệ."}), 400
        
    if not (file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
        return jsonify({"error": "Định dạng file không hợp lệ. Chỉ hỗ trợ file Excel (.xlsx, .xls)."}), 400
        
    try:
        filepath = os.path.join(WORKSPACE_DIR, filename)
        file.save(filepath)
        
        with CACHE_LOCK:
            update_all_caches()
            if BACKLOG_CACHE_RAW and "error" not in BACKLOG_CACHE_RAW["aging"] and "error" not in BACKLOG_CACHE_RAW["treo"]:
                add_to_history(BACKLOG_CACHE_RAW["aging"], BACKLOG_CACHE_RAW["treo"])
                
        return jsonify({"success": True, "message": f"Tải lên và đồng bộ file {filename} thành công!"})
    except Exception as e:
        return jsonify({"error": f"Lỗi lưu file hoặc cập nhật cache: {str(e)}"}), 500

@app.route('/api/sync', methods=['POST'])
@requires_auth
def trigger_sync():
    global OPERATIONAL_CACHE, OPR_CACHE, BACKLOG_CACHE_RAW, UNSTABLE_PO_CACHE, OFF_SPE_CACHE
    with CACHE_LOCK:
        if is_admin():
            # Load config and download Google Sheets
            config = load_config()
            download_errors = []
            
            # Mapping URLs to local file names
            mappings = [
                ("ops_url", 'Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', "Báo cáo Vận hành"),
                ("opr_url", 'OPR TTS.xlsx', "OPR TTS"),
                ("aging_url", 'Aging _5 ngày.xlsx', "Aging > 5 ngày"),
                ("treo_url", 'Treo luân chuyển GIAO_TRẢ by IMTHIR.xlsx', "Treo luân chuyển"),
                ("bat_on_url", 'buu_cuc_bat_on.xlsx', "Bưu cục bất ổn"),
                ("off_spe_url", 'off_tuyen_spe.xlsx', "OFF tuyến SPE"),
                ("tao_don_url", 'vols_tao_don.xlsx', "Volume tạo đơn")
            ]
            
            for key, filename, label in mappings:
                url = config.get(key, "")
                if url and url.strip():
                    filepath = os.path.join(WORKSPACE_DIR, filename)
                    success, msg = download_google_sheet(url, filepath)
                    if not success:
                        download_errors.append(f"{label}: {msg}")
                        
            if download_errors:
                return jsonify({"error": "Lỗi đồng bộ Google Sheets:\n" + "\n".join(download_errors)}), 400
                
        update_all_caches()
        
        if OPERATIONAL_CACHE and "error" in OPERATIONAL_CACHE:
            return jsonify({"error": OPERATIONAL_CACHE["error"]}), 400
        if OPR_CACHE and "error" in OPR_CACHE:
            return jsonify({"error": OPR_CACHE["error"]}), 400
        if BACKLOG_CACHE_RAW:
            if "error" in BACKLOG_CACHE_RAW["aging"]:
                return jsonify({"error": BACKLOG_CACHE_RAW["aging"]["error"]}), 400
            if "error" in BACKLOG_CACHE_RAW["treo"]:
                return jsonify({"error": BACKLOG_CACHE_RAW["treo"]["error"]}), 400
        if UNSTABLE_PO_CACHE and "error" in UNSTABLE_PO_CACHE:
            # We only raise a sync error if the file is expected (i.e. url is configured or file exists)
            # otherwise it can fallback to empty/error message in its own panel
            pass
                
        ts = add_to_history(BACKLOG_CACHE_RAW["aging"], BACKLOG_CACHE_RAW["treo"])
    return jsonify({"success": True, "timestamp": ts})

@app.route('/api/summary-dashboard')
@requires_auth
def api_summary_dashboard():
    try:
        df_gtc, df_ltc, df_aging, df_treo = get_dataframes()
        
        # Filters from query params
        am = request.args.get('am')
        province = request.args.get('province')
        post_office = request.args.get('post_office')
        selected_date = request.args.get('date')
        
        # Find latest date dynamically
        all_times = set(df_gtc['Time'].dropna().unique()).union(set(df_ltc['Time'].dropna().unique()))
        dates_sorted = sorted(list(all_times), key=lambda x: pd.to_datetime(x.split(' - ')[0]))
        if not dates_sorted:
            return jsonify({"error": "Không có dữ liệu ngày trong Datagtc hoặc Dataltc"})
            
        if selected_date and selected_date in dates_sorted:
            latest_date = selected_date
        else:
            latest_date = dates_sorted[-1]
        
        prev_date = dates_sorted[-2] if len(dates_sorted) >= 2 else None
        
        # Find same day of week last week (7 days ago)
        latest_dt = pd.to_datetime(latest_date.split(' - ')[0])
        last_week_date = None
        for d in dates_sorted:
            dt = pd.to_datetime(d.split(' - ')[0])
            if (latest_dt - dt).days == 7:
                last_week_date = d
                break
                
        def compute_kpi_for_date(date_str, filter_am=None, filter_prov=None, filter_po=None):
            if not date_str:
                return None
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
        
        # Filter for latest date
        today_gtc = df_gtc[df_gtc['Time'] == latest_date]
        today_ltc = df_ltc[df_ltc['Time'] == latest_date]
        
        # Apply filters to today's data
        today_gtc = apply_filters(today_gtc, am, province, post_office)
        today_ltc = apply_filters(today_ltc, am, province, post_office)
        
        # Apply filters to backlog datasets
        curr_aging = apply_filters(df_aging, am, province, post_office)
        curr_treo = apply_filters(df_treo, am, province, post_office)
        
        # 1. Completed Volume Grouped by Province
        gtc_prov = today_gtc.groupby('mapped_prov').agg({'Volume': 'sum', 'delivered_vol': 'sum', 'ttc_vol': 'sum'}).reset_index()
        ltc_prov = today_ltc.groupby('mapped_prov').agg({'Volume': 'sum', 'ltc_vol': 'sum'}).reset_index()
        
        merged_prov = pd.merge(gtc_prov, ltc_prov, on='mapped_prov', suffixes=('_gtc', '_ltc'), how='outer').fillna(0)
        completed_vols = []
        for _, r in merged_prov.iterrows():
            prov_name = r['mapped_prov']
            completed_vols.append({
                'province': prov_name,
                'LTC': int(r['ltc_vol']),
                'GTC': int(r['delivered_vol']),
                'TTC': int(r['ttc_vol']),
                'LTC_pct': round((r['ltc_vol'] / r['Volume_ltc'] * 100), 2) if r['Volume_ltc'] > 0 else 0.0,
                'GTC_pct': round((r['delivered_vol'] / r['Volume_gtc'] * 100), 2) if r['Volume_gtc'] > 0 else 0.0,
                'TTC_pct': round((r['ttc_vol'] / r['Volume_gtc'] * 100), 2) if r['Volume_gtc'] > 0 else 0.0,
                'Volume_gtc': int(r['Volume_gtc']),
                'Volume_ltc': int(r['Volume_ltc'])
            })
            
        # 2. Backlog by AM
        treo_giao = curr_treo[curr_treo['Loại đơn'] == 'Luân chuyển giao']
        treo_tra = curr_treo[curr_treo['Loại đơn'] == 'Luân chuyển trả']
        
        aging_am = curr_aging.groupby('mapped_am').size().reset_index(name='chua_giao')
        treo_giao_am = treo_giao.groupby('mapped_am').size().reset_index(name='chua_lay')
        treo_tra_am = treo_tra.groupby('mapped_am').size().reset_index(name='chua_tra')
        
        backlog_am = pd.merge(treo_giao_am, aging_am, on='mapped_am', how='outer')
        backlog_am = pd.merge(backlog_am, treo_tra_am, on='mapped_am', how='outer').fillna(0)
        
        backlog_by_am = []
        for _, r in backlog_am.iterrows():
            backlog_by_am.append({
                'am': r['mapped_am'],
                'chua_lay': int(r['chua_lay']),
                'chua_giao': int(r['chua_giao']),
                'chua_tra': int(r['chua_tra'])
            })
            
        # 3. Overall & Province-specific KPIs
        kpis = {}
        
        def format_kpi_dict(latest_kpi, prev_kpi, lw_kpi):
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
                        'ttc': round(latest_kpi['ttc'] - prev_kpi['ttc'], 2)
                    }
                else:
                    res['dod'] = None
                
                if lw_kpi:
                    res['wow'] = {
                        'ltc': round(latest_kpi['ltc'] - lw_kpi['ltc'], 2),
                        'gtc': round(latest_kpi['gtc'] - lw_kpi['gtc'], 2),
                        'ttc': round(latest_kpi['ttc'] - lw_kpi['ttc'], 2)
                    }
                else:
                    res['wow'] = None
            else:
                res['dod'] = None
                res['wow'] = None
            return res
            
        overall_latest = compute_kpi_for_date(latest_date, am, province, post_office)
        overall_prev = compute_kpi_for_date(prev_date, am, province, post_office) if prev_date else None
        overall_lw = compute_kpi_for_date(last_week_date, am, province, post_office) if last_week_date else None
        
        kpis['overall'] = format_kpi_dict(overall_latest, overall_prev, overall_lw)
        
        # Compute for each province
        all_provinces = set(df_ltc['mapped_prov'].unique()).union(set(df_gtc['mapped_prov'].unique()))
        for prov_name in all_provinces:
            if prov_name == "Không xác định":
                continue
            prov_latest = compute_kpi_for_date(latest_date, am, prov_name, post_office)
            prov_prev = compute_kpi_for_date(prev_date, am, prov_name, post_office) if prev_date else None
            prov_lw = compute_kpi_for_date(last_week_date, am, prov_name, post_office) if last_week_date else None
            
            clean_key = clean_str_key(prov_name)
            kpis[clean_key] = format_kpi_dict(prov_latest, prov_prev, prov_lw)
            kpis[clean_key]['name'] = prov_name
            
        return jsonify(clean_nan({
            'latest_date': latest_date,
            'all_dates': dates_sorted[::-1],
            'completed_vols': completed_vols,
            'backlog_by_am': backlog_by_am,
            'kpis': kpis
        }))
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": f"Lỗi tính toán summary: {str(e)}"}), 500

@app.route('/api/trends-dashboard')
@requires_auth
def api_trends_dashboard():
    try:
        df_gtc, df_ltc, _, _ = get_dataframes()
        
        am = request.args.get('am')
        province = request.args.get('province')
        post_office = request.args.get('post_office')
        
        # Apply filters
        df_gtc = apply_filters(df_gtc, am, province, post_office)
        df_ltc = apply_filters(df_ltc, am, province, post_office)
        
        # Find last 7 dates sorted chronologically
        all_times = set(df_gtc['Time'].dropna().unique()).union(set(df_ltc['Time'].dropna().unique()))
        dates_sorted = sorted(list(all_times), key=lambda x: pd.to_datetime(x.split(' - ')[0]))
        last_7_dates = dates_sorted[-7:]
        
        # Filter both dataframes to last 7 dates
        df_gtc_7 = df_gtc[df_gtc['Time'].isin(last_7_dates)]
        df_ltc_7 = df_ltc[df_ltc['Time'].isin(last_7_dates)]
        
        # Group by mapped_prov and Time
        gtc_grouped = df_gtc_7.groupby(['mapped_prov', 'Time']).agg({'Volume': 'sum', 'delivered_vol': 'sum'}).reset_index()
        ltc_grouped = df_ltc_7.groupby(['mapped_prov', 'Time']).agg({'Volume': 'sum', 'ltc_vol': 'sum'}).reset_index()
        
        # Overall trends
        gtc_overall = df_gtc_7.groupby('Time').agg({'Volume': 'sum', 'delivered_vol': 'sum'}).reset_index()
        ltc_overall = df_ltc_7.groupby('Time').agg({'Volume': 'sum', 'ltc_vol': 'sum'}).reset_index()
        
        res_dates = last_7_dates
        
        trends = {}
        all_provinces = set(df_ltc_7['mapped_prov'].unique()).union(set(df_gtc_7['mapped_prov'].unique()))
        
        for prov in all_provinces:
            if prov == "Không xác định":
                continue
            prov_ltc = []
            prov_gtc = []
            
            p_ltc_df = ltc_grouped[ltc_grouped['mapped_prov'] == prov]
            p_gtc_df = gtc_grouped[gtc_grouped['mapped_prov'] == prov]
            
            for d in res_dates:
                # LTC
                d_ltc = p_ltc_df[p_ltc_df['Time'] == d]
                if len(d_ltc) > 0 and d_ltc['Volume'].iloc[0] > 0:
                    prov_ltc.append(round((d_ltc['ltc_vol'].iloc[0] / d_ltc['Volume'].iloc[0] * 100), 2))
                else:
                    prov_ltc.append(None)
                # GTC
                d_gtc = p_gtc_df[p_gtc_df['Time'] == d]
                if len(d_gtc) > 0 and d_gtc['Volume'].iloc[0] > 0:
                    prov_gtc.append(round((d_gtc['delivered_vol'].iloc[0] / d_gtc['Volume'].iloc[0] * 100), 2))
                else:
                    prov_gtc.append(None)
                    
            trends[prov] = {
                'ltc': prov_ltc,
                'gtc': prov_gtc
            }
            
        # Overall
        overall_ltc = []
        overall_gtc = []
        for d in res_dates:
            d_ltc = ltc_overall[ltc_overall['Time'] == d]
            if len(d_ltc) > 0 and d_ltc['Volume'].iloc[0] > 0:
                overall_ltc.append(round((d_ltc['ltc_vol'].iloc[0] / d_ltc['Volume'].iloc[0] * 100), 2))
            else:
                overall_ltc.append(None)
                
            d_gtc = gtc_overall[gtc_overall['Time'] == d]
            if len(d_gtc) > 0 and d_gtc['Volume'].iloc[0] > 0:
                overall_gtc.append(round((d_gtc['delivered_vol'].iloc[0] / d_gtc['Volume'].iloc[0] * 100), 2))
            else:
                overall_gtc.append(None)
                
        trends['overall'] = {
            'ltc': overall_ltc,
            'gtc': overall_gtc
        }
        
        return jsonify(clean_nan({
            'dates': res_dates,
            'trends': trends
        }))
        
    except Exception as e:
        return jsonify({"error": f"Lỗi tính toán xu hướng: {str(e)}"}), 500

@app.route('/api/matrix-tables')
@requires_auth
def api_matrix_tables():
    try:
        df_gtc, df_ltc, _, _ = get_dataframes()
        
        am_filter = request.args.get('am')
        province_filter = request.args.get('province')
        post_office_filter = request.args.get('post_office')
        
        # Apply filters
        df_gtc_f = apply_filters(df_gtc, am_filter, province_filter, post_office_filter)
        df_ltc_f = apply_filters(df_ltc, am_filter, province_filter, post_office_filter)
        
        # Find last 6 dates available
        all_times = set(df_gtc['Time'].dropna().unique()).union(set(df_ltc['Time'].dropna().unique()))
        dates_sorted = sorted(list(all_times), key=lambda x: pd.to_datetime(x.split(' - ')[0]))
        last_6_dates = dates_sorted[-6:][::-1]
        
        def build_matrix_data(df, vol_col, target_val_col):
            df_6 = df[df['Time'].isin(last_6_dates)].copy()
            if len(df_6) == 0:
                return {'dates': last_6_dates, 'rows': []}
                
            # Group by AM, Chi tiết, Time
            grouped = df_6.groupby(['mapped_am', 'Chi tiết', 'Time']).agg({'Volume': 'sum', target_val_col: 'sum'}).reset_index()
            
            # AM overall totals for each date
            am_totals = df_6.groupby(['mapped_am', 'Time']).agg({'Volume': 'sum', target_val_col: 'sum'}).reset_index()
            
            rows = []
            unique_ams = sorted(df_6['mapped_am'].unique())
            
            for am in unique_ams:
                if am == "Không xác định":
                    continue
                
                am_time_df = am_totals[am_totals['mapped_am'] == am]
                totals_dict = {}
                for d in last_6_dates:
                    d_row = am_time_df[am_time_df['Time'] == d]
                    if len(d_row) > 0:
                        vol = float(d_row['Volume'].iloc[0])
                        target_val = float(d_row[target_val_col].iloc[0])
                        pct = round((target_val / vol * 100), 2) if vol > 0 else 0.0
                        totals_dict[d] = {'vol': int(vol), 'pct': pct}
                    else:
                        totals_dict[d] = {'vol': 0, 'pct': 0.0}
                        
                am_details_df = grouped[grouped['mapped_am'] == am]
                unique_pos = sorted(am_details_df['Chi tiết'].unique())
                pos_list = []
                
                for po in unique_pos:
                    po_time_df = am_details_df[am_details_df['Chi tiết'] == po]
                    po_data_dict = {}
                    for d in last_6_dates:
                        d_row = po_time_df[po_time_df['Time'] == d]
                        if len(d_row) > 0:
                            vol = float(d_row['Volume'].iloc[0])
                            target_val = float(d_row[target_val_col].iloc[0])
                            pct = round((target_val / vol * 100), 2) if vol > 0 else 0.0
                            po_data_dict[d] = {'vol': int(vol), 'pct': pct}
                        else:
                            po_data_dict[d] = {'vol': 0, 'pct': 0.0}
                    pos_list.append({
                        'bc': po,
                        'data': po_data_dict
                    })
                    
                rows.append({
                    'am': am,
                    'is_header': True,
                    'totals': totals_dict,
                    'pos': pos_list
                })
                
            return {
                'dates': last_6_dates,
                'rows': rows
            }
            
        ltc_matrix = build_matrix_data(df_ltc_f, 'Volume', 'ltc_vol')
        gtc_matrix = build_matrix_data(df_gtc_f, 'Volume', 'delivered_vol')
        
        return jsonify(clean_nan({
            'ltc': ltc_matrix,
            'gtc': gtc_matrix
        }))
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": f"Lỗi tính toán matrix tables: {str(e)}"}), 500

@app.route('/api/chat', methods=['POST'])
@requires_auth
def api_chat():
    try:
        data = request.json or {}
        message = data.get('message', '').strip().lower()
        
        if not message:
            return jsonify({"reply": "Chào bạn! Mình có thể giúp gì cho bạn hôm nay?"})
            
        global OPERATIONAL_CACHE, OPR_CACHE
        # Ensure caches are loaded
        with CACHE_LOCK:
            if OPERATIONAL_CACHE is None:
                try:
                    OPERATIONAL_CACHE = process_operational_report()
                except Exception as e:
                    print(f"Error loading ops cache for chat: {e}")
            if OPR_CACHE is None:
                try:
                    OPR_CACHE = process_opr_report()
                except Exception as e:
                    print(f"Error loading opr cache for chat: {e}")
                    
        # Parse queries
        # 1. Bưu cục tệ nhất (Worst Post Office)
        if 'tệ nhất' in message or 'te nhat' in message or 'kém nhất' in message or 'kem nhat' in message:
            reply = "Dựa trên dữ liệu vận hành mới nhất:<br>"
            # GTC Worst
            if OPERATIONAL_CACHE and 'worst_10_gtc' in OPERATIONAL_CACHE and OPERATIONAL_CACHE['worst_10_gtc']:
                worst_gtc = OPERATIONAL_CACHE['worst_10_gtc'][0]
                reply += f"📍 **Bưu cục có tỷ lệ Giao thành công (GTC) thấp nhất**: <br><strong>{worst_gtc['Chi tiết']}</strong> với tỷ lệ GTC chỉ đạt <strong>{worst_gtc['% GTC']:.2f}%</strong> (Sản lượng: {int(worst_gtc['Volume'])} đơn).<br>"
            else:
                reply += "📍 Không tìm thấy dữ liệu bưu cục GTC.<br>"
                
            # LTC Worst
            if OPERATIONAL_CACHE and 'worst_10_ltc' in OPERATIONAL_CACHE and OPERATIONAL_CACHE['worst_10_ltc']:
                worst_ltc = OPERATIONAL_CACHE['worst_10_ltc'][0]
                reply += f"📍 **Bưu cục có tỷ lệ Giao lần đầu (LTC) thấp nhất**: <br><strong>{worst_ltc['Chi tiết']}</strong> với tỷ lệ LTC đạt <strong>{worst_ltc['% LTC']:.2f}%</strong> (Sản lượng: {int(worst_ltc['Volume'])} đơn).<br>"
                
            # Worst ODR (Ontime Delivery) from ODR TTS.csv
            try:
                odr_path = os.path.join(WORKSPACE_DIR, 'ODR TTS.csv')
                if os.path.exists(odr_path):
                    df_odr = pd.read_csv(odr_path)
                    df_odr['GTC'] = pd.to_numeric(df_odr['GTC'], errors='coerce')
                    df_odr['%Ontime'] = pd.to_numeric(df_odr['%Ontime'].astype(str).str.rstrip('%'), errors='coerce') / 100
                    latest_date = df_odr['Time'].max()
                    df_latest = df_odr[(df_odr['Time'] == latest_date) & (df_odr['GTC'] >= 10)] # filter at least 10 orders
                    if not df_latest.empty:
                        worst_odr_row = df_latest.sort_values(by='%Ontime', ascending=True).iloc[0]
                        reply += f"📍 **Bưu cục trễ hẹn (ODR thấp nhất) ngày {latest_date}**: <br><strong>{worst_odr_row['Chi tiết']}</strong> với tỷ lệ Đúng giờ chỉ đạt <strong>{worst_odr_row['%Ontime']*100:.2f}%</strong> (Sản lượng: {int(worst_odr_row['GTC'])} đơn)."
            except Exception as e:
                print(f"Error computing worst ODR for chat: {e}")
                
            return jsonify({"reply": reply})

        # 2. OPR (Operational Performance Rate)
        elif 'opr' in message:
            if OPR_CACHE and 'overall_opr' in OPR_CACHE:
                opr_val = OPR_CACHE['overall_opr']
                reply = f"📊 **Tỷ lệ hiệu suất OPR ngày hôm nay**: đạt <strong>{opr_val}%</strong>.<br>"
                try:
                    val_float = float(str(opr_val).replace('%', ''))
                    if val_float >= 80:
                        reply += "✅ Hiệu suất OPR đạt mục tiêu tối thiểu (Target: >= 80%). Các bưu cục đang vận hành khá tốt!"
                    else:
                        reply += "⚠️ Hiệu suất OPR hiện tại chưa đạt mục tiêu tối thiểu (Target: >= 80%). Cần tập trung cải thiện thời gian xử lý đơn hàng."
                except:
                    pass
            else:
                reply = "📊 Hiện tại hệ thống chưa cập nhật đủ dữ liệu OPR hôm nay."
            return jsonify({"reply": reply})
            
        # 3. ODR (Ontime Delivery Rate)
        elif 'odr' in message or 'đúng giờ' in message or 'trễ' in message or 'tre' in message or 'dung gio' in message:
            try:
                odr_path = os.path.join(WORKSPACE_DIR, 'ODR TTS.csv')
                if os.path.exists(odr_path):
                    df_odr = pd.read_csv(odr_path)
                    df_odr['GTC'] = pd.to_numeric(df_odr['GTC'], errors='coerce')
                    df_odr['%Ontime'] = pd.to_numeric(df_odr['%Ontime'].astype(str).str.rstrip('%'), errors='coerce') / 100
                    df_odr['ontime_vol'] = df_odr['GTC'] * df_odr['%Ontime']
                    latest_date = df_odr['Time'].max()
                    df_latest = df_odr[df_odr['Time'] == latest_date]
                    if not df_latest.empty:
                        overall_odr = (df_latest['ontime_vol'].sum() / df_latest['GTC'].sum()) * 100
                        total_vol = df_latest['GTC'].sum()
                        reply = f"🚚 **Tỷ lệ Giao hàng đúng giờ (ODR) ngày {latest_date}**: đạt <strong>{overall_odr:.2f}%</strong> (Trên tổng sản lượng {int(total_vol):,} đơn giao).<br>"
                        if overall_odr >= 90:
                            reply += "🎉 Tỷ lệ giao hàng đúng giờ duy trì ở mức cao và đạt chuẩn chất lượng dịch vụ của GHN!"
                        else:
                            reply += "⚠️ Tỷ lệ giao đúng giờ đang giảm, vui lòng kiểm tra các tuyến luân chuyển bị nghẽn."
                    else:
                        reply = "🚚 Chưa có dữ liệu ODR cho ngày hôm nay."
                else:
                    reply = "🚚 Không tìm thấy file dữ liệu ODR TTS.csv để tính toán."
            except Exception as e:
                reply = f"🚚 Lỗi tính toán tỷ lệ ODR: {str(e)}"
            return jsonify({"reply": reply})

        # 4. GTC / LTC / Tổng quan
        elif 'gtc' in message or 'giao thành công' in message:
            if OPERATIONAL_CACHE and 'overall_gtc' in OPERATIONAL_CACHE:
                gtc_val = OPERATIONAL_CACHE['overall_gtc']
                reply = f"✅ **Tỷ lệ Giao thành công (GTC) hôm nay**: đạt <strong>{gtc_val}%</strong>.<br>(Target đề ra: >= 60.0%)"
            else:
                reply = "✅ Chưa có dữ liệu Giao thành công hôm nay."
            return jsonify({"reply": reply})

        elif 'ltc' in message or 'giao lần đầu' in message:
            if OPERATIONAL_CACHE and 'overall_ltc' in OPERATIONAL_CACHE:
                ltc_val = OPERATIONAL_CACHE['overall_ltc']
                reply = f"✈️ **Tỷ lệ Giao lần đầu thành công (LTC) hôm nay**: đạt <strong>{ltc_val}%</strong>."
            else:
                reply = "✈️ Chưa có dữ liệu Giao lần đầu thành công hôm nay."
            return jsonify({"reply": reply})

        # 5. Backlog / Tồn đọng
        elif 'backlog' in message or 'tồn' in message or 'chưa giao' in message:
            try:
                df_gtc, df_ltc, df_aging, df_treo = get_dataframes()
                total_aging = len(df_aging) if df_aging is not None else 0
                total_treo = len(df_treo) if df_treo is not None else 0
                reply = f"📦 **Tổng đơn tồn đọng (Backlog) hiện tại**: <strong>{total_aging + total_treo:,} đơn</strong>.<br>"
                reply += f"- Đơn giao trễ (Aging > 5 ngày): <strong>{total_aging:,} đơn</strong>.<br>"
                reply += f"- Đơn bị treo luân chuyển stuck: <strong>{total_treo:,} đơn</strong>."
            except Exception as e:
                reply = f"📦 Lỗi tính toán đơn backlog: {str(e)}"
            return jsonify({"reply": reply})
            
        else:
            # Help reply
            reply = "🤖 **Trợ lý NTB** xin chào!<br>Mình hỗ trợ trả lời nhanh các câu hỏi vận hành. Bạn có thể hỏi:<br>"
            reply += "- 📍 Bưu cục nào vận hành **tệ nhất**?<br>"
            reply += "- 📊 Tỷ lệ hiệu suất **OPR** hôm nay?<br>"
            reply += "- 🚚 Tỷ lệ giao hàng đúng giờ **ODR**?<br>"
            reply += "- 📦 Tổng số đơn **backlog** tồn đọng?<br>"
            reply += "- ✅ Tỷ lệ **GTC** hoặc **LTC** hiện tại?"
            return jsonify({"reply": reply})
            
    except Exception as ex:
        return jsonify({"reply": f"🤖 Đã xảy ra lỗi hệ thống: {str(ex)}"}), 500

@app.route('/api/ntb-structure')
@requires_auth
def get_ntb_structure():
    try:
        path = os.path.join(WORKSPACE_DIR, 'co_cau_ntb.xlsx')
        if not os.path.exists(path):
            return jsonify({"error": "Không tìm thấy file co_cau_ntb.xlsx"})
        
        df = pd.read_excel(path, sheet_name='Sheet1')
        df['Tỉnh'] = df['Tỉnh'].replace({'Khánh Hoà': 'Khánh Hòa', 'Bình Phước': 'Lâm Đồng'}).fillna("Chưa xác định").str.strip()
        df['AM'] = df['AM'].fillna("Chưa có AM").str.strip()
        df['Bưu cục'] = df['Bưu cục'].fillna("Chưa xác định").str.strip()
        
        structure = {}
        for prov, p_df in df.groupby('Tỉnh'):
            structure[prov] = {}
            for am, a_df in p_df.groupby('AM'):
                structure[prov][am] = sorted(list(a_df['Bưu cục'].unique()))
                
        return jsonify(structure)
    except Exception as e:
        return jsonify({"error": f"Lỗi đọc file cơ cấu: {str(e)}"}), 500

@app.route('/api/files-status')
@requires_auth
def get_files_status():
    files = [
        'Aging _5 ngày.xlsx',
        'Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx',
        'OPR TTS.xlsx',
        'Treo luân chuyển GIAO_TRẢ by IMTHIR.xlsx',
        'buu_cuc_bat_on.xlsx',
        'co_cau_ntb.xlsx',
        'off_tuyen_spe.xlsx',
        'vols_tao_don.xlsx'
    ]
    status = []
    for f in files:
        path = os.path.join(WORKSPACE_DIR, f)
        if os.path.exists(path):
            stat = os.stat(path)
            mtime = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            size_mb = round(stat.st_size / (1024 * 1024), 2)
            status.append({"name": f, "exists": True, "mtime": mtime, "size_mb": size_mb})
        else:
            status.append({"name": f, "exists": False, "mtime": "-", "size_mb": 0})
    return jsonify(status)
@app.route('/api/volume-creation')
@requires_auth
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

if __name__ == '__main__':
    # Optimize to only run heavy startup tasks once when Flask debug mode is active
    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        def startup_cache_init():
            update_all_caches()
            with CACHE_LOCK:
                # Initialize history with a sync if it is empty
                history = load_history()
                if not history and BACKLOG_CACHE_RAW:
                    aging = BACKLOG_CACHE_RAW["aging"]
                    treo = BACKLOG_CACHE_RAW["treo"]
                    if "error" not in aging and "error" not in treo:
                        add_to_history(aging, treo)
        threading.Thread(target=startup_cache_init, daemon=True).start()
            
    print("Dashboard server starts on http://127.0.0.1:5000/")
    app.run(debug=False, host='127.0.0.1', port=5000)

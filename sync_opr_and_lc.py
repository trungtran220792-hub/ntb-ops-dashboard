import os
import sys
import unicodedata
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gspread
from google.oauth2.service_account import Credentials

# Configure output encoding for Vietnamese characters
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

from dotenv import load_dotenv

# Paths
load_dotenv()

JSON_FILE = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') or r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
if not os.path.exists(JSON_FILE):
    JSON_FILE = 'credentials.json'

SHEET_ID = os.environ.get('SHEET_ID') or '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU'
DESKTOP_DIR = os.path.join(os.path.expanduser('~'), 'Desktop')

print("="*60)
print("BẮT ĐẦU CHẠY PIPELINE TÍNH TOÁN OPR TTS & RỚT LC VỚI ĐỊNH DẠNG GOOGLE SHEETS & BIỂU ĐỒ NATIVE")
print("="*60)

# 1. Connect to Google Sheets
print("Đang kết nối tới Google Sheets...")
try:
    creds = Credentials.from_service_account_file(
        JSON_FILE, 
        scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    )
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SHEET_ID)
    print(f"✔️ Đã kết nối thành công tới spreadsheet: '{sh.title}'")
except Exception as e:
    print(f"❌ Lỗi kết nối Google Sheets: {e}")
    sys.exit(1)

# Helper to read worksheet
def get_df_from_sheet(sheet_name):
    print(f"-> Đang tải dữ liệu thô từ sheet '{sheet_name}'...")
    ws = sh.worksheet(sheet_name)
    data = ws.get_all_values(value_render_option='UNFORMATTED_VALUE')
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data[1:], columns=data[0])

# 2. Load Raw Worksheets
try:
    df_opr = get_df_from_sheet('OPR TTS')
    df_lc = get_df_from_sheet('data rớt LC')
    if not df_lc.empty:
        df_lc = df_lc.iloc[:, :8]
    df_cocau = get_df_from_sheet('cocau')
    print("✔️ Đã tải xong dữ liệu thô.")
except Exception as e:
    print(f"❌ Lỗi tải các worksheet: {e}")
    sys.exit(1)

# 3. Standardize and Map AM Names
def normalize_name(name):
    if pd.isna(name):
        return ""
    return unicodedata.normalize('NFC', str(name).strip()).upper()

df_cocau['Bưu cục_norm'] = df_cocau['Bưu cục'].apply(normalize_name)
df_cocau['BC_norm'] = df_cocau['BC'].apply(normalize_name)

# Create robust mapping dicts
bc_to_am = {}
for _, r in df_cocau.iterrows():
    am_val = str(r['Am']).strip()
    bc_to_am[r['BC_norm']] = am_val
for _, r in df_cocau.iterrows():
    am_val = str(r['Am']).strip()
    bc_to_am[r['Bưu cục_norm']] = am_val

def map_am_robust(bc_name):
    norm = normalize_name(bc_name)
    if not norm:
        return "Unknown"
    if norm in bc_to_am:
        return bc_to_am[norm]
    # Substring matching
    for k, v in bc_to_am.items():
        if k in norm or norm in k:
            return v
    return "Unknown"

# Normalize df_opr columns
df_opr.columns = [str(c).strip() for c in df_opr.columns]
opr_cols_lower = {c.lower(): c for c in df_opr.columns}
opr_rename = {}
if 'ngayltc' in opr_cols_lower:
    opr_rename[opr_cols_lower['ngayltc']] = 'NgayLTC'

if 'vol_ltc' in opr_cols_lower:
    opr_rename[opr_cols_lower['vol_ltc']] = 'vol_ltc'
elif 'don_ltc' in opr_cols_lower:
    opr_rename[opr_cols_lower['don_ltc']] = 'vol_ltc'
elif 'don ltc' in opr_cols_lower:
    opr_rename[opr_cols_lower['don ltc']] = 'vol_ltc'
    
if 'ot' in opr_cols_lower:
    opr_rename[opr_cols_lower['ot']] = 'ot'
elif 'don_ontime' in opr_cols_lower:
    opr_rename[opr_cols_lower['don_ontime']] = 'ot'
elif 'don ontime' in opr_cols_lower:
    opr_rename[opr_cols_lower['don ontime']] = 'ot'
    
if 'am' in opr_cols_lower:
    opr_rename[opr_cols_lower['am']] = 'AM'
    
if 'tutinh' in opr_cols_lower:
    opr_rename[opr_cols_lower['tutinh']] = 'tutinh'
elif 'tu tinh' in opr_cols_lower:
    opr_rename[opr_cols_lower['tu tinh']] = 'tutinh'
    
if 'kholay' in opr_cols_lower:
    opr_rename[opr_cols_lower['kholay']] = 'kholay'
elif 'kho lay' in opr_cols_lower:
    opr_rename[opr_cols_lower['kho lay']] = 'kholay'

if 'tuần' in opr_cols_lower:
    opr_rename[opr_cols_lower['tuần']] = 'Tuần'
elif 'tuan' in opr_cols_lower:
    opr_rename[opr_cols_lower['tuan']] = 'Tuần'

if opr_rename:
    df_opr = df_opr.rename(columns=opr_rename)

for col in ['NgayLTC', 'vol_ltc', 'ot', 'AM']:
    if col not in df_opr.columns:
        df_opr[col] = np.nan if col in ['NgayLTC', 'AM'] else 0.0

if 'kholay' not in df_opr.columns:
    df_opr['kholay'] = ""

if 'Tuần' not in df_opr.columns:
    df_opr['NgayLTC_dt'] = pd.to_datetime(df_opr['NgayLTC'], errors='coerce')
    df_opr['Tuần'] = 'W' + df_opr['NgayLTC_dt'].dt.isocalendar().week.astype(str)

if 'Khung giờ' not in df_opr.columns:
    if 'Khung giờ tạo' in df_opr.columns:
        df_opr['Khung giờ'] = df_opr['Khung giờ tạo']
    elif 'khung_gio_tao' in df_opr.columns:
        df_opr['Khung giờ'] = df_opr['khung_gio_tao']
    else:
        df_opr['Khung giờ'] = ""

# Map AM
df_opr['mapped_AM'] = df_opr['kholay'].apply(map_am_robust)
df_lc['mapped_AM'] = df_lc['Chi tiết'].apply(map_am_robust)

# Clean and parse columns
df_opr['vol_ltc'] = pd.to_numeric(df_opr['vol_ltc'], errors='coerce').fillna(0)
df_opr['ot'] = pd.to_numeric(df_opr['ot'], errors='coerce').fillna(0)

df_lc['Vol cần LC'] = pd.to_numeric(df_lc['Vol cần LC'], errors='coerce').fillna(0)
def parse_pct(val):
    if pd.isna(val) or val == "":
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    val_str = str(val).strip().replace('%', '')
    try:
        val_str = val_str.replace(',', '.')
        return float(val_str) / 100.0
    except:
        return 0.0
df_lc['pct_float'] = df_lc['%_rot_lc'].apply(parse_pct)
df_lc['Vol rớt LC'] = df_lc['Vol cần LC'] * df_lc['pct_float']

# =========================================================================
# CALCULATIONS & WRITING TO GOOGLE SHEETS
# =========================================================================

# 1. OPR TTS Calculations
print("Calculating OPR TTS summaries...")
# Filter for current week (W24)
df_opr_w24 = df_opr[df_opr['Tuần'] == 'W24'].copy()

# Group by AM and Khung giờ
opr_grouped = df_opr_w24.groupby(['mapped_AM', 'Khung giờ']).agg(
    Tong_Don=('vol_ltc', 'sum'),
    Don_Dung_Han=('ot', 'sum')
).reset_index()
opr_grouped['%OPR'] = (opr_grouped['Don_Dung_Han'] / opr_grouped['Tong_Don']).fillna(0)

# Reshape to WIDE format for easier viewing and charting in Google Sheets
# Pivot table with AM as index and Khung giờ as columns
pivot_df = opr_grouped.pivot(index='mapped_AM', columns='Khung giờ', values=['Tong_Don', 'Don_Dung_Han', '%OPR']).fillna(0)

# Flatten columns: e.g., ('Tong_Don', '1.Tạo từ 9h-19h') -> 'Tong_Don_9h_19h'
pivot_df.columns = [f"{col[0]}_{'9h_19h' if '9h-19h' in col[1] else '19h_9h'}" for col in pivot_df.columns]
pivot_df = pivot_df.reset_index()

# Sort by Daytime OPR descending
pivot_df = pivot_df.sort_values(by='%OPR_9h_19h', ascending=False)

# Prepare upload matrix (writing raw floats/integers)
opr_headers = [
    "AM", 
    "Tổng đơn (9h-19h)", "Đúng hạn (9h-19h)", "%OPR (9h-19h)",
    "Tổng đơn (19h-9h)", "Đúng hạn (19h-9h)", "%OPR (19h-9h)"
]
opr_upload_rows = [opr_headers]
for _, row in pivot_df.iterrows():
    opr_upload_rows.append([
        row['mapped_AM'],
        int(row['Tong_Don_9h_19h']),
        int(row['Don_Dung_Han_9h_19h']),
        float(row['%OPR_9h_19h']),
        int(row['Tong_Don_19h_9h']),
        int(row['Don_Dung_Han_19h_9h']),
        float(row['%OPR_19h_9h'])
    ])

# 2. Leftover LC (Rớt LC) Calculations
print("Calculating Leftover LC summaries...")
# WoW Comparison
lc_wow = df_lc[df_lc['Tuần'].isin(['Tuần 23', 'Tuần 24'])].groupby('Tuần').agg(
    Vol_Can=('Vol cần LC', 'sum'),
    Vol_Rot=('Vol rớt LC', 'sum')
).reset_index()
lc_wow['% rớt LC'] = (lc_wow['Vol_Rot'] / lc_wow['Vol_Can']).fillna(0)
lc_wow = lc_wow.sort_values(by='Tuần')

lc_wow_rows = []
w23_pct, w24_pct = 0.0, 0.0
for _, row in lc_wow.iterrows():
    lc_wow_rows.append([
        row['Tuần'],
        int(round(row['Vol_Can'])),
        int(round(row['Vol_Rot'])),
        float(row['% rớt LC'])
    ])
    if row['Tuần'] == 'Tuần 23':
        w23_pct = row['% rớt LC']
    elif row['Tuần'] == 'Tuần 24':
        w24_pct = row['% rớt LC']

diff_pct = w24_pct - w23_pct
lc_wow_rows.append([
    "So sánh W24 vs W23 (Chênh lệch)",
    "",
    "",
    float(diff_pct)
])

# Top 20 Post Offices for W24
df_lc_w24 = df_lc[df_lc['Tuần'] == 'Tuần 24'].copy()
po_grouped = df_lc_w24.groupby('Chi tiết').agg(
    Vol_Can=('Vol cần LC', 'sum'),
    Vol_Rot=('Vol rớt LC', 'sum')
).reset_index()
po_grouped['% rớt LC'] = (po_grouped['Vol_Rot'] / po_grouped['Vol_Can']).fillna(0)
top_20_po = po_grouped.sort_values(by='% rớt LC', ascending=False).head(20)

lc_top20_rows = []
for idx, (_, row) in enumerate(top_20_po.iterrows(), start=1):
    lc_top20_rows.append([
        idx,
        row['Chi tiết'],
        int(round(row['Vol_Can'])),
        int(round(row['Vol_Rot'])),
        float(row['% rớt LC'])
    ])

# =========================================================================
# WRITE AND FORMAT GOOGLE SHEETS
# =========================================================================

def write_and_format_sheet(sheet_name, data, formats_callback):
    try:
        # Check if worksheet exists, if so delete it
        try:
            ws = sh.worksheet(sheet_name)
            sh.del_worksheet(ws)
            print(f"-> Đã xóa sheet cũ '{sheet_name}'")
        except gspread.exceptions.WorksheetNotFound:
            pass
        
        num_rows = max(len(data) + 15, 60)
        num_cols = max(len(data[0]) + 15, 20)
        ws = sh.add_worksheet(title=sheet_name, rows=str(num_rows), cols=str(num_cols))
        
        # Write values
        ws.update(range_name='A1', values=data, value_input_option='USER_ENTERED')
        
        # Set gridlines
        sh.batch_update({
            "requests": [
                {
                    "updateSheetProperties": {
                        "properties": {
                            "sheetId": ws.id,
                            "gridProperties": {
                                "hideGridlines": False
                            }
                        },
                        "fields": "gridProperties.hideGridlines"
                    }
                }
            ]
        })
        
        # Invoke formatting callback
        formats_callback(ws, len(data))
        print(f"✔️ Đã ghi & định dạng thành công sheet '{sheet_name}'")
        return ws.id
    except Exception as e:
        print(f"❌ Lỗi ghi/định dạng sheet '{sheet_name}': {e}")
        return None

# Formatting callback for OPR TTS Summary
def format_opr_summary(ws, num_rows):
    # Header format
    ws.format("A1:G1", {
        "backgroundColor": {"red": 30/255, "green": 41/255, "blue": 59/255}, # slate blue
        "horizontalAlignment": "CENTER",
        "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontFamily": "Segoe UI", "fontSize": 11}
    })
    
    # Body font format
    ws.format(f"A2:G{num_rows}", {
        "textFormat": {"fontFamily": "Segoe UI", "fontSize": 10}
    })
    
    # Alignments
    ws.format(f"A2:A{num_rows}", {"horizontalAlignment": "LEFT"})
    ws.format(f"B2:C{num_rows}", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
    ws.format(f"D2:D{num_rows}", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "PERCENT", "pattern": "0.0%"}})
    ws.format(f"E2:F{num_rows}", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
    ws.format(f"G2:G{num_rows}", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "PERCENT", "pattern": "0.0%"}})
    
    # Set alternating background colors (zebra rows) for easier reading
    requests = []
    for r in range(2, num_rows + 1):
        color = {"red": 248/255, "green": 250/255, "blue": 252/255} if r % 2 == 0 else {"red": 1.0, "green": 1.0, "blue": 1.0}
        requests.append({
            "repeatCell": {
                "range": {"sheetId": ws.id, "startRowIndex": r-1, "endRowIndex": r, "startColumnIndex": 0, "endColumnIndex": 7},
                "cell": {"userEnteredFormat": {"backgroundColor": color}},
                "fields": "userEnteredFormat.backgroundColor"
            }
        })
    sh.batch_update({"requests": requests})

# Formatting callback for Rớt LC Summary
def format_lc_summary(ws, num_rows):
    # Sheet titles
    ws.format("A1", {"textFormat": {"bold": True, "fontFamily": "Segoe UI", "fontSize": 14, "foregroundColor": {"red": 15/255, "green": 23/255, "blue": 42/255}}})
    ws.format("A3", {"textFormat": {"bold": True, "fontFamily": "Segoe UI", "fontSize": 12, "foregroundColor": {"red": 30/255, "green": 41/255, "blue": 59/255}}})
    ws.format("A9", {"textFormat": {"bold": True, "fontFamily": "Segoe UI", "fontSize": 12, "foregroundColor": {"red": 30/255, "green": 41/255, "blue": 59/255}}})
    
    # Table 1: WoW comparison (A4:D4)
    ws.format("A4:D4", {
        "backgroundColor": {"red": 30/255, "green": 41/255, "blue": 59/255},
        "horizontalAlignment": "CENTER",
        "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontFamily": "Segoe UI", "fontSize": 11}
    })
    ws.format("A5:D7", {"textFormat": {"fontFamily": "Segoe UI", "fontSize": 10}})
    ws.format("A5:A7", {"horizontalAlignment": "LEFT"})
    ws.format("B5:C7", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
    ws.format("D5:D7", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "PERCENT", "pattern": "0.00%"}})
    
    # Table 2: Top 20 (A11:E11)
    ws.format("A11:E11", {
        "backgroundColor": {"red": 30/255, "green": 41/255, "blue": 59/255},
        "horizontalAlignment": "CENTER",
        "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontFamily": "Segoe UI", "fontSize": 11}
    })
    ws.format("A12:E31", {"textFormat": {"fontFamily": "Segoe UI", "fontSize": 10}})
    ws.format("A12:A31", {"horizontalAlignment": "CENTER"})
    ws.format("B12:B31", {"horizontalAlignment": "LEFT"})
    ws.format("C12:D31", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
    ws.format("E12:E31", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "PERCENT", "pattern": "0.00%"}})
    
    # Formatting the comparison row (A7:D7) to highlight it
    ws.format("A7:D7", {
        "textFormat": {"bold": True, "foregroundColor": {"red": 220/255, "green": 38/255, "blue": 38/255}}, # Red text
        "backgroundColor": {"red": 254/255, "green": 242/255, "blue": 242/255} # light red background
    })
    
    # Alternating row color for Top 20
    requests = []
    for r in range(12, 32):
        color = {"red": 248/255, "green": 250/255, "blue": 252/255} if r % 2 == 0 else {"red": 1.0, "green": 1.0, "blue": 1.0}
        requests.append({
            "repeatCell": {
                "range": {"sheetId": ws.id, "startRowIndex": r-1, "endRowIndex": r, "startColumnIndex": 0, "endColumnIndex": 5},
                "cell": {"userEnteredFormat": {"backgroundColor": color}},
                "fields": "userEnteredFormat.backgroundColor"
            }
        })
    sh.batch_update({"requests": requests})

# Write the sheets
opr_ws_id = write_and_format_sheet('OPR TTS Summary', opr_upload_rows, format_opr_summary)

lc_upload_rows = [
    ["BÁO CÁO TỔNG HỢP RỚT LC VÙNG NTB"],
    [],
    ["1. SO SÁNH SỐ LIỆU TỔNG HỢP VỚI TUẦN TRƯỚC (W23 vs W24)"],
    ["Tuần", "Tổng Vol cần LC", "Tổng Vol rớt LC", "% rớt LC"],
]
lc_upload_rows.extend(lc_wow_rows)
lc_upload_rows.extend([[], []])
lc_upload_rows.append(["2. TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LC CAO NHẤT (TUẦN 24)"])
lc_upload_rows.append(["STT", "Bưu cục (Chi tiết)", "Tổng Vol cần LC", "Tổng Vol rớt LC", "% rớt LC"])
lc_upload_rows.extend(lc_top20_rows)

lc_ws_id = write_and_format_sheet('Rớt LC Summary', lc_upload_rows, format_lc_summary)

# =========================================================================
# CREATING NATIVE GOOGLE SHEETS CHARTS
# =========================================================================
print("Đang tạo biểu đồ Google Sheets tương tác trực quan...")

chart_requests = []

if opr_ws_id:
    # Chart 1: Grouped Column Chart for OPR TTS by AM & Timeframe
    # Domain is Column A (AM names) row 2 to endRowIndex
    # Series 1 is Column D (%OPR Daytime 9h-19h)
    # Series 2 is Column G (%OPR Nighttime 19h-9h)
    end_idx = len(opr_upload_rows)
    chart1 = {
        "addChart": {
            "chart": {
                "spec": {
                    "title": "HIỆU SUẤT OPR TTS THEO AM VÀ KHUNG GIỜ (W24)",
                    "titleTextFormat": {"fontFamily": "Segoe UI", "fontSize": 14, "bold": True},
                    "basicChart": {
                        "chartType": "COLUMN",
                        "legendPosition": "BOTTOM_LEGEND",
                        "headerCount": 1,
                        "axis": [
                            {"position": "BOTTOM_AXIS", "title": "Area Manager (AM)"},
                            {"position": "LEFT_AXIS", "title": "Tỷ lệ OPR (%)"}
                        ],
                        "domains": [
                            {"domain": {"sourceRange": {"sources": [{"sheetId": opr_ws_id, "startRowIndex": 0, "endRowIndex": end_idx, "startColumnIndex": 0, "endColumnIndex": 1}]}}}
                        ],
                        "series": [
                            {"series": {"sourceRange": {"sources": [{"sheetId": opr_ws_id, "startRowIndex": 0, "endRowIndex": end_idx, "startColumnIndex": 3, "endColumnIndex": 4}]}}, "targetAxis": "LEFT_AXIS"},
                            {"series": {"sourceRange": {"sources": [{"sheetId": opr_ws_id, "startRowIndex": 0, "endRowIndex": end_idx, "startColumnIndex": 6, "endColumnIndex": 7}]}}, "targetAxis": "LEFT_AXIS"}
                        ]
                    }
                },
                "position": {
                    "overlayPosition": {
                        "anchorCell": {"sheetId": opr_ws_id, "rowIndex": 1, "columnIndex": 8}, # Column I
                        "offsetXPixels": 20, "offsetYPixels": 0
                    }
                }
            }
        }
    }
    chart_requests.append(chart1)

if lc_ws_id:
    # Chart 2: Horizontal Bar Chart for Top 20 Post Offices rớt LC
    # Domain is Column B (Bưu cục name, rows 12 to 31, 0-indexed: index 11 to 31)
    # Series is Column E (% rớt LC, rows 11 to 31)
    chart2 = {
        "addChart": {
            "chart": {
                "spec": {
                    "title": "TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LC CAO NHẤT (W24)",
                    "titleTextFormat": {"fontFamily": "Segoe UI", "fontSize": 14, "bold": True},
                    "basicChart": {
                        "chartType": "BAR", # Horizontal Bar
                        "legendPosition": "NO_LEGEND",
                        "headerCount": 1,
                        "axis": [
                            {"position": "BOTTOM_AXIS", "title": "Tỷ lệ rớt LC (%)"},
                            {"position": "LEFT_AXIS", "title": "Bưu cục"}
                        ],
                        "domains": [
                            {"domain": {"sourceRange": {"sources": [{"sheetId": lc_ws_id, "startRowIndex": 10, "endRowIndex": 31, "startColumnIndex": 1, "endColumnIndex": 2}]}}}
                        ],
                        "series": [
                            {"series": {"sourceRange": {"sources": [{"sheetId": lc_ws_id, "startRowIndex": 10, "endRowIndex": 31, "startColumnIndex": 4, "endColumnIndex": 5}]}}, "targetAxis": "BOTTOM_AXIS"}
                        ]
                    }
                },
                "position": {
                    "overlayPosition": {
                        "anchorCell": {"sheetId": lc_ws_id, "rowIndex": 3, "columnIndex": 6}, # Column G, next to WoW table
                        "offsetXPixels": 20, "offsetYPixels": 0
                    }
                }
            }
        }
    }
    chart_requests.append(chart2)

if chart_requests:
    try:
        sh.batch_update({"requests": chart_requests})
        print("✔️ Đã vẽ biểu đồ động trực tuyến thành công lên Google Sheets.")
    except Exception as e:
        print(f"❌ Lỗi chèn biểu đồ Google Sheets: {e}")

# =========================================================================
# PREMIUM PLOTS GENERATION FOR LOCAL DESKTOP EXPORTS
# =========================================================================

# Matplotlib styling for white/light theme
plt.style.use('default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['figure.facecolor'] = '#FFFFFF'
plt.rcParams['axes.facecolor'] = '#FFFFFF'
plt.rcParams['text.color'] = '#1F2937'
plt.rcParams['axes.labelcolor'] = '#4B5563'
plt.rcParams['xtick.color'] = '#4B5563'
plt.rcParams['ytick.color'] = '#4B5563'

# Chart 1: OPR TTS by AM & Timeframe (W24)
print("Vẽ biểu đồ OPR TTS cục bộ...")
unique_ams = pivot_df['mapped_AM'].unique()

daytime_rates_list = []
nighttime_rates_list = []
valid_ams = []

for am in unique_ams:
    row = pivot_df[pivot_df['mapped_AM'] == am].iloc[0]
    # Filter out AMs with almost zero total volume
    tot_vol = row['Tong_Don_9h_19h'] + row['Tong_Don_19h_9h']
    if tot_vol < 10:
        continue
    daytime_rates_list.append(row['%OPR_9h_19h'])
    nighttime_rates_list.append(row['%OPR_19h_9h'])
    valid_ams.append(am)

x = np.arange(len(valid_ams))
width = 0.35

fig, ax = plt.subplots(figsize=(15, 7.5))

# Use modern vibrant colors
rects1 = ax.bar(x - width/2, [r * 100 for r in daytime_rates_list], width, label='Daytime (9h-19h)', color='#4F46E5', alpha=0.9)
rects2 = ax.bar(x + width/2, [r * 100 for r in nighttime_rates_list], width, label='Nighttime (19h-9h)', color='#F59E0B', alpha=0.9)

ax.set_ylabel('Hiệu suất OPR (%)', fontsize=12, fontweight='bold', labelpad=10)
ax.set_title('HIỆU SUẤT OPR TTS THEO AM VÀ KHUNG GIỜ GIEO (W24)', fontsize=15, fontweight='bold', pad=25, color='#111827')
ax.set_xticks(x)
ax.set_xticklabels(valid_ams, rotation=40, ha='right', fontsize=10.5)
ax.set_ylim(0, 115)

ax.grid(axis='y', linestyle=':', alpha=0.5, color='#D1D5DB', zorder=0)
for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#D1D5DB')

ax.legend(frameon=False, loc='upper right', fontsize=11)

def autolabel(rects, text_color):
    for rect in rects:
        height = rect.get_height()
        if height > 0:
            ax.annotate(f'{height:.1f}%',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold', color=text_color)

autolabel(rects1, '#3730A3')
autolabel(rects2, '#92400E')

fig.tight_layout()
opr_chart_path = os.path.join(DESKTOP_DIR, "OPR_TTS_theo_AM_va_Khung_Gio.png")
plt.savefig(opr_chart_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✔️ Đã lưu biểu đồ OPR TTS tại: {opr_chart_path}")


# Chart 2: Top 20 Post Offices for Leftover LC (W24)
print("Vẽ biểu đồ Top 20 Bưu cục rớt LC cục bộ...")
top_20_sorted = top_20_po.sort_values(by='% rớt LC', ascending=True)

fig, ax = plt.subplots(figsize=(12, 8.5))

y_pos = np.arange(len(top_20_sorted))
bars = ax.barh(y_pos, [r * 100 for r in top_20_sorted['% rớt LC']], align='center', color='#F43F5E', alpha=0.9, height=0.6)

ax.set_yticks(y_pos)
ax.set_yticklabels(top_20_sorted['Chi tiết'], fontsize=10, fontweight='medium')
ax.set_xlabel('Tỷ lệ rớt LC (%)', fontsize=12, fontweight='bold', labelpad=10)
ax.set_title('TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LC CAO NHẤT (W24)', fontsize=15, fontweight='bold', pad=25, color='#111827')

max_val = max(top_20_sorted['% rớt LC'] * 100)
ax.set_xlim(0, max(max_val * 1.15, 10))
ax.grid(axis='x', linestyle=':', alpha=0.5, color='#D1D5DB', zorder=0)

for spine in ['top', 'right', 'bottom']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#D1D5DB')

for bar in bars:
    width_val = bar.get_width()
    if width_val > 0:
        ax.annotate(f'{width_val:.2f}%',
                    xy=(width_val, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0),
                    textcoords="offset points",
                    ha='left', va='center', fontsize=9.5, fontweight='bold', color='#9F1239')

fig.tight_layout()
lc_chart_path = os.path.join(DESKTOP_DIR, "Top_20_Buu_Cuc_Rot_LC.png")
plt.savefig(lc_chart_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✔️ Đã lưu biểu đồ Top 20 Bưu cục rớt LC tại: {lc_chart_path}")

print("="*60)
print("Pipeline calculation and premium report generation completed successfully!")
print("="*60)

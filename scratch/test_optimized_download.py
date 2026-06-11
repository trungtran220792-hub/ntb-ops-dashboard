import urllib.request
import re
import os
import time
import concurrent.futures

spreadsheet_id = "1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ"
edit_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'

sheet_mappings = [
    (["data"], "ops_gtc.csv"),
    (["dataltc", "rawltc", "data ltc"], "ops_ltc.csv"),
    (["cocauvung", "cơ cấu", "co_cau", "co cau"], "ops_co_cau.csv"),
    (["cocauvung", "cơ cấu", "co_cau", "co cau"], "co_cau_ntb.csv"),
    (["tts"], "ops_tts.csv"),
    (["opr"], "opr_opr.csv"),
    (["raw n-1", "oe_madh", "raw_n-1", "raw n - 1", "oe madh"], "opr_oe.csv"),
    (["rawopr"], "opr_raw.csv"),
    (["aging trên 5 ngày", "aging tren 5 ngay", "đơn giao aging trên 5 ngày", "don giao aging tren 5 ngay"], "aging_raw.csv"),
    (["treo lc", "stuck", "treo luân chuyển", "treo luan chuyen"], "treo_stuck.csv"),
    (["ntb", "bất ổn", "bat_on", "cảnh báo"], "buu_cuc_bat_on.csv"),
    (["đang off", "dang off", "off", "off_tuyen", "off tuyến"], "off_tuyen_spe.csv"),
    (["shopee_tiktok", "tao_don", "tạo đơn"], "vols_tao_don.csv"),
    (["odr tts", "odr_tts"], "ODR TTS.csv"),
    (["nhân sự", "nhan su"], "ops_nhan_su.csv")
]

start_time = time.time()

# Step 1: Fetch HTML
req = urllib.request.Request(edit_url, headers={'User-Agent': user_agent})
with urllib.request.urlopen(req, timeout=15) as r:
    html = r.read().decode('utf-8')

# Regex to find sheet GIDs and names
pattern = r'\[\s*\d+\s*,\s*0\s*,\s*\\"?(\d+)\\"?\s*,\s*\[\s*\{\s*\\"?1\\"?\s*:\s*\[\s*\[\s*0\s*,\s*0\s*,\s*\\"?([^\\"\(\]]+)\\"?'
matches = re.findall(pattern, html)

gid_map = {}
for gid, name in matches:
    name_clean = name.strip().lower()
    gid_map[name_clean] = gid

# Group filenames by GID to avoid duplicate downloads
gid_to_filenames = {}
for candidates, target_csv in sheet_mappings:
    matched_gid = None
    for cand in candidates:
        cand_clean = cand.strip().lower()
        if cand_clean in gid_map:
            matched_gid = gid_map[cand_clean]
            break
            
    if matched_gid is not None:
        if matched_gid not in gid_to_filenames:
            gid_to_filenames[matched_gid] = []
        gid_to_filenames[matched_gid].append(target_csv)

print(f"Unique GIDs to download: {len(gid_to_filenames)}")

# Download function
def download_gid(gid, filenames):
    t_start = time.time()
    csv_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid}"
    req = urllib.request.Request(csv_url, headers={'User-Agent': user_agent})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read()
        for fname in filenames:
            output_path = os.path.join("scratch", fname)
            with open(output_path, 'wb') as f:
                f.write(content)
        print(f"Downloaded GID {gid} for {filenames} in {time.time() - t_start:.2f}s")
        return True
    except Exception as e:
        print(f"Error downloading GID {gid}: {e}")
        return False

# Download in parallel using max_workers matching the number of unique GIDs (11 workers)
with concurrent.futures.ThreadPoolExecutor(max_workers=len(gid_to_filenames)) as executor:
    futures = [executor.submit(download_gid, gid, fnames) for gid, fnames in gid_to_filenames.items()]
    results = [f.result() for f in concurrent.futures.as_completed(futures)]

print(f"Optimized Sync completed in {time.time() - start_time:.2f} seconds!")

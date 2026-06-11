import os
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

files_to_delete = [
    'Aging _5 ngày.xlsx',
    'Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx',
    'OPR TTS.xlsx',
    'Treo luân chuyển GIAO_TRẢ by IMTHIR.xlsx',
    'buu_cuc_bat_on.xlsx',
    'off_tuyen_spe.xlsx',
    'vols_tao_don.xlsx',
    'temp_ops_check.xlsx',
    'test_aging.xlsx',
    'test_aging_url.xlsx',
    'test_bat_on_url.xlsx',
    'test_off_spe_url.xlsx',
    'test_opr.xlsx',
    'test_opr_url.xlsx',
    'test_ops.xlsx',
    'test_ops_url.xlsx',
    'test_tao_don_url.xlsx',
    'test_treo_url.xlsx',
    'test_urllib.xlsx',
    'api_response_check.txt',
    'server_output.log',
    'server_output_new.log'
]

print("Deleting large Excel files...")
for f in files_to_delete:
    if os.path.exists(f):
        try:
            os.remove(f)
            print(f"Deleted successfully: {f.encode('utf-8', errors='ignore').decode('utf-8')}")
        except Exception as e:
            print(f"Error deleting: {str(e)}")

print("\nDeleting cache .pkl files...")
pkl_files = glob.glob("*.pkl")
for pkl in pkl_files:
    try:
        os.remove(pkl)
        print(f"Deleted cache file: {pkl}")
    except Exception as e:
        print(f"Error deleting cache: {str(e)}")

print("Cleanup complete.")

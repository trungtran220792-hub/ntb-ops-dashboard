import sys
sys.path.append('.')

sys.stdout.reconfigure(encoding='utf-8')

from app import process_operational_report

res = process_operational_report()
if "error" in res:
    print("Error:", res["error"])
else:
    print("overall_gan:", res.get("overall_gan"))
    print("overall_gtc:", res.get("overall_gtc"))
    print("overall_ltc:", res.get("overall_ltc"))
    print("total_volume:", res.get("total_volume"))

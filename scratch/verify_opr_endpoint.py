import sys
sys.path.append('.')
from app import process_opr_report

print("Testing process_opr_report without filters...")
res = process_opr_report()
if "error" in res:
    print(f"Error: {res['error']}")
    sys.exit(1)

print(f"Total Volume: {res.get('total_volume')}")
print(f"Total Ontime: {res.get('total_ontime')}")
print(f"Total Late: {res.get('total_late')}")
print(f"Overall OPR: {res.get('overall_opr')}%")
print(f"Delta N-1: {res.get('delta_n1')}%")
print(f"Delta WK: {res.get('delta_wk')}%")
print(f"AM performance sample: {res.get('am_performance')[:2] if res.get('am_performance') else []}")

print("\nTesting process_opr_report with AM filter: Huỳnh Tấn Hiển...")
res_am = process_opr_report(am="Huỳnh Tấn Hiển")
print(f"Total Volume (Filtered): {res_am.get('total_volume')}")
print(f"Overall OPR (Filtered): {res_am.get('overall_opr')}%")

print("\nTesting process_opr_report with Province filter: Bình Thuận...")
res_prov = process_opr_report(province="Bình Thuận")
print(f"Total Volume (Filtered): {res_prov.get('total_volume')}")
print(f"Overall OPR (Filtered): {res_prov.get('overall_opr')}%")

print("\nAll tests completed successfully!")

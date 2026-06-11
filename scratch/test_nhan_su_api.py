import requests
import sys

def test_nhan_su():
    sys.stdout.reconfigure(encoding='utf-8')
    session = requests.Session()
    # Login
    login_url = "http://127.0.0.1:5000/api/login"
    login_res = session.post(login_url, json={"username": "admin", "password": "admin123"})
    print("Login response status:", login_res.status_code)
    try:
        print("Login response json:", login_res.json())
    except Exception as e:
        print("Login JSON error:", e)

    # Query nhan-su
    ns_url = "http://127.0.0.1:5000/api/nhan-su"
    ns_res = session.get(ns_url)
    print("Nhan-su API response status:", ns_res.status_code)
    if ns_res.status_code == 200:
        data = ns_res.json()
        print("Active Headcount:", data.get("active_headcount"))
        print("Resigned Headcount:", data.get("resigned_headcount"))
        print("PO Count:", data.get("po_count"))
        pos = data.get("pos", [])
        print("Total POs in list:", len(pos))
        if pos:
            # Avoid printing Vietnamese directly if not clean
            first_po = pos[0]
            print("First PO clean details:")
            for k, v in first_po.items():
                print(f"  {k}: {repr(v)}")
    else:
        print("Error content:", ns_res.text)

if __name__ == "__main__":
    test_nhan_su()

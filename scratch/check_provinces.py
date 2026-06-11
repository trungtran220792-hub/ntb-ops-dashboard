import requests

r = requests.get('http://127.0.0.1:5000/api/summary-dashboard', auth=('admin', 'admin123'))
data = r.json()

print(f"Total completed_vols: {len(data['completed_vols'])}")
for idx, item in enumerate(data['completed_vols']):
    prov = item.get('province')
    print(f"Index {idx}: type={type(prov)}, is_none={prov is None}, repr={repr(prov)}")

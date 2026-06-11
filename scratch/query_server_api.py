import requests
import json

base_url = 'http://127.0.0.1:5000'

# We first try to query /api/matrix-tables without auth, if it needs auth, we'll see.
# In app.py:
# @app.route('/api/matrix-tables')
# @requires_permission('tab-volume-creation')
# Wait, requires_permission checks session, but for script compatibility, it accepts Basic Auth.
# Let's use basic auth for admin:admin123
auth = ('admin', 'admin123')

try:
    print("Fetching /api/matrix-tables...")
    res = requests.get(f"{base_url}/api/matrix-tables", auth=auth)
    print("Status code:", res.status_code)
    if res.status_code == 200:
        data = res.json()
        print("Keys in response:", list(data.keys()))
        
        # Search for targets in ltc and gtc matrix
        targets = [
            'Điểm Xử Lý Hàng Thôn 2-Xã Nhân Cơ-Đắk Nông',
            'Điểm Xử Lý Hàng TDP 8 Quốc Lộ 14-Đông Gia Nghĩa-Lâm Đồng',
            'Điểm lấy hàng Nguyễn Đình Chiểu-Nghĩa Tân-Gia Nghĩa-Đăk Nông'
        ]
        
        results = []
        for key in ['ltc', 'gtc']:
            matrix = data.get(key, {})
            rows = matrix.get('rows', [])
            results.append(f"\n=== Matrix: {key} ===")
            results.append(f"Number of rows: {len(rows)}")
            
            # Print unique AMs in the response
            unique_ams = [r.get('am') for r in rows]
            results.append(f"Unique AMs in response: {unique_ams}")
            
            for row in rows:
                am = row.get('am')
                pos = row.get('pos', [])
                for po in pos:
                    po_name = po.get('bc')
                    if any(t.lower() in po_name.lower() for t in targets):
                        results.append(f"Found match: PO='{po_name}' under AM='{am}'")
                        results.append(f"Data: {po.get('data')}")
                        
        with open('scratch/server_api_response.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(results))
        print("Saved to scratch/server_api_response.txt")
    else:
        print("Error response text:", res.text)
except Exception as e:
    print("Error querying server:", e)

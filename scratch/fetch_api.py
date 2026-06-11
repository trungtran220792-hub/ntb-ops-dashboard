import requests

url = "http://127.0.0.1:5000/api/matrix-tables?time_group=ngay"
auth = ('admin', 'admin123')

try:
    print("Fetching from local server...")
    r = requests.get(url, auth=auth, timeout=10)
    r.raise_for_status()
    data = r.json()
    
    # Search for the target post offices in matrix data
    targets = ['TDP 8', 'Thôn 2', 'Nguyễn Đình Chiểu']
    out = []
    
    for type_key in ['ltc', 'gtc']:
        matrix = data.get(type_key, {})
        rows = matrix.get('rows', [])
        out.append(f"\n=== {type_key.upper()} Matrix ===")
        out.append(f"Number of rows (AMs): {len(rows)}")
        
        found_any = False
        for row in rows:
            am_name = row.get('am', '')
            pos = row.get('pos', [])
            for po in pos:
                bc_name = po.get('bc', '')
                if any(t.lower() in bc_name.lower() for t in targets):
                    out.append(f"Found match: BC='{bc_name}' under AM='{am_name}'")
                    found_any = True
        if not found_any:
            out.append("No matches found in this matrix!")
            
    with open('api_response_check.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    print("Done!")

except Exception as e:
    with open('api_response_check.txt', 'w', encoding='utf-8') as f:
        f.write(f"Error fetching API: {e}")
    print(f"Error: {e}")

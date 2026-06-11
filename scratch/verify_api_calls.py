import sys
sys.path.append('.')
import json
from app import app, get_dataframes

print("Initializing cache...")
get_dataframes(force=True)
print("Cache initialized.")

client = app.test_client()

with client.session_transaction() as sess:
    sess['username'] = 'admin'
    sess['role'] = 'admin'
    sess['permissions'] = ['tab-dashboard']

res_summary = client.get('/api/summary-dashboard?time_group=tuan')
if res_summary.status_code == 200:
    with open('scratch/summary_tuan.json', 'w', encoding='utf-8') as f:
        json.dump(res_summary.get_json(), f, indent=2, ensure_ascii=False)
    print("Wrote summary_tuan.json")

res_trends = client.get('/api/trends-dashboard?time_group=tuan')
if res_trends.status_code == 200:
    with open('scratch/trends_tuan.json', 'w', encoding='utf-8') as f:
        json.dump(res_trends.get_json(), f, indent=2, ensure_ascii=False)
    print("Wrote trends_tuan.json")

import sys
sys.path.append('.')
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')
from app import app, get_dataframes
print("Loading cache...")
get_dataframes(force=True)
print("Cache loaded.")

client = app.test_client()

with client.session_transaction() as sess:
    sess['username'] = 'admin'
    sess['role'] = 'admin'
    sess['permissions'] = ['tab-dashboard']

res_summary = client.get('/api/summary-dashboard?time_group=ngay')
if res_summary.status_code == 200:
    data = res_summary.get_json()
    with open('scratch/summary_ngay.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Wrote summary_ngay.json")
    print("Latest Date:", data.get('latest_date'))
    overall = data.get('kpis', {}).get('overall', {})
    print("Overall LTC:", overall.get('ltc'))
    print("Overall GTC:", overall.get('gtc'))
    print("n-3 Overall comparison:", overall.get('n3'))
else:
    print("Error:", res_summary.status_code, res_summary.get_data(as_text=True))

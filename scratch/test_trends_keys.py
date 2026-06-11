import sys
sys.path.append('.')
import json
from app import app, get_dataframes

# Initialize cache manually
print("Initializing cache...")
get_dataframes(force=True)
print("Cache initialized.")

client = app.test_client()

with client.session_transaction() as sess:
    sess['username'] = 'admin'
    sess['role'] = 'admin'
    sess['permissions'] = ['tab-dashboard']

response = client.get('/api/trends-dashboard')
print("Status code:", response.status_code)

with open('scratch/test_trends_output.txt', 'w', encoding='utf-8') as f:
    f.write(f"Status code: {response.status_code}\n")
    if response.status_code == 200:
        data = response.get_json()
        f.write("Keys in trends:\n")
        for key in data.get('trends', {}).keys():
            f.write(f"  {repr(key)}\n")
    else:
        f.write("Response body:\n")
        f.write(response.get_data(as_text=True))
print("Wrote output to scratch/test_trends_output.txt")

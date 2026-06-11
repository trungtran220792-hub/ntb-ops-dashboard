import sys
import os
sys.path.append(os.getcwd())
sys.stdout.reconfigure(encoding='utf-8')

from app import app, api_summary_dashboard, get_dataframes
from flask import session

# Load cache in this process
get_dataframes(force=True)

with app.test_request_context('/api/summary-dashboard?time_group=ngay'):
    session['username'] = 'admin'
    session['role'] = 'admin'
    response = api_summary_dashboard()
    if isinstance(response, tuple):
        res_obj, status_code = response
        print("Status Code:", status_code)
        print(res_obj.get_data(as_text=True))
    else:
        print(response.get_data(as_text=True))

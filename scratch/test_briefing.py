import sys
import traceback
from app import app, get_overall_metrics_summary

with app.app_context():
    try:
        print("Calling get_overall_metrics_summary()...")
        res = get_overall_metrics_summary()
        print("Result:", res)
    except Exception as e:
        print("Exception occurred:")
        traceback.print_exc()

# -*- coding: utf-8 -*-
import os
import re

cache_dir = r"C:\Users\lap4all\.gemini\antigravity-browser-profile\Default\Cache\Cache_Data"
files = ["f_0003ea", "f_0003f5", "f_000410"]

queries = ["renderNtbAnalysisTable", "setAmOprSort", "renderOprAmChartOnly", "tbody-ntb-ltc-analysis"]

for f in files:
    path = os.path.join(cache_dir, f)
    if os.path.exists(path):
        print(f"\nChecking cache file: {f}")
        print(f"  Size: {os.path.getsize(path)} bytes")
        
        # Read file as bytes (since it's cache data, it might contain some binary headers)
        with open(path, 'rb') as file:
            data = file.read()
            
        # Try to search query strings in bytes
        for q in queries:
            q_bytes = q.encode('utf-8')
            if q_bytes in data:
                count = data.count(q_bytes)
                print(f"  Found '{q}': {count} occurrences")
    else:
        print(f"File {f} not found")

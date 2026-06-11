# -*- coding: utf-8 -*-
import os

filepath = r"c:\Users\lap4all\Desktop\New folder\app.py"
outpath = r"c:\Users\lap4all\Desktop\New folder\scratch\app_endpoints_code.txt"

if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open(outpath, 'w', encoding='utf-8') as out_f:
        # Search and write summary-dashboard route
        idx = content.find("@app.route('/api/summary-dashboard')")
        if idx != -1:
            out_f.write("=== SUMMARY DASHBOARD ENDPOINT ===\n")
            out_f.write(content[idx:idx+8000])
            out_f.write("\n\n" + "="*80 + "\n\n")
            
        # Search and write trends-dashboard route
        idx = content.find("@app.route('/api/trends-dashboard')")
        if idx != -1:
            out_f.write("=== TRENDS DASHBOARD ENDPOINT ===\n")
            out_f.write(content[idx:idx+8000])
            out_f.write("\n\n" + "="*80 + "\n\n")
            
        # Search and write matrix-tables route
        idx = content.find("@app.route('/api/matrix-tables')")
        if idx != -1:
            out_f.write("=== MATRIX TABLES ENDPOINT ===\n")
            out_f.write(content[idx:idx+8000])
            out_f.write("\n\n" + "="*80 + "\n\n")
            
        # Search and write OPR route
        idx = content.find("@app.route('/api/opr')")
        if idx != -1:
            out_f.write("=== OPR ENDPOINT ===\n")
            out_f.write(content[idx:idx+8000])
            out_f.write("\n\n" + "="*80 + "\n\n")
            
    print("API endpoints code extracted to app_endpoints_code.txt")
else:
    print("app.py not found")

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if "df_gtc['Tỉnh']" in line or "df_gtc['AM']" in line or "df_gtc['am']" in line or "df_gtc['tỉnh']" in line:
            print(f"Line {idx+1}: {line.strip()}")

import zipfile
import os

zip_path = r"c:\Users\lap4all\Desktop\New folder\dashboard_update.zip"
out_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"

if os.path.exists(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as z:
        if 'templates/index.html' in z.namelist():
            z.extract('templates/index.html', out_dir)
            extracted_path = os.path.join(out_dir, 'templates', 'index.html')
            print(f"Extracted to {extracted_path}")
            
            with open(extracted_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print("Extracted file size:", len(content))
            
            terms = ["tab-opr", "opr-overall-rate", "setAmOprSort", "renderOprAmChartOnly", "Báo Cáo Hiệu Suất OPR TTS"]
            for term in terms:
                if term in content:
                    print(f"Found term '{term}' in extracted index.html!")
                else:
                    print(f"Did NOT find term '{term}' in extracted index.html.")
        else:
            print("templates/index.html not in zip.")
else:
    print("Zip file not found.")

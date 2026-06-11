import os

file_path = r"c:\Users\lap4all\Desktop\New folder\scratch\index_changes_ntb.txt"

if os.path.exists(file_path):
    print("Found index_changes_ntb.txt. Reading...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print("File size:", len(content))
    terms = ["tab-opr", "opr-overall-rate", "setAmOprSort", "renderOprAmChartOnly", "Báo Cáo Hiệu Suất OPR TTS"]
    for term in terms:
        print(f"Term '{term}': {'yes' if term in content else 'no'}")
else:
    print("index_changes_ntb.txt not found.")

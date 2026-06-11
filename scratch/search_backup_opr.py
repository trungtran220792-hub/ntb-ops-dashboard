import os

scratch_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"

search_terms = ["tab-opr", "opr-overall-rate", "setAmOprSort", "renderOprAmChartOnly", "Báo Cáo Hiệu Suất OPR TTS", "BÃ¡o CÃ¡o Hiá»‡u Suáº¥t OPR TTS"]

res_lines = []

for file_name in os.listdir(scratch_dir):
    file_path = os.path.join(scratch_dir, file_name)
    if not os.path.isfile(file_path):
        continue
        
    # Read file with multiple encodings
    encodings = ['utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 'latin-1']
    content = None
    used_enc = None
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                content = f.read()
                used_enc = enc
                break
        except Exception:
            continue
            
    if content is None:
        res_lines.append(f"Could not read {file_name}\n")
        continue
        
    # Search
    found = []
    for term in search_terms:
        if term in content:
            found.append(term)
            
    if found:
        res_lines.append(f"File {file_name} ({used_enc}, size {len(content)} chars) contains: {found}\n")
        lines = content.split('\n')
        for i, line in enumerate(lines):
            for term in found:
                if term in line:
                    res_lines.append(f"  Line {i+1}: {line[:150].strip()}\n")
                    break

with open(os.path.join(scratch_dir, "search_opr_res.txt"), 'w', encoding='utf-8') as f_out:
    f_out.writelines(res_lines)

print("Search completed. Output written to scratch/search_opr_res.txt")

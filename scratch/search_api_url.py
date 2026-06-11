import os

index_path = 'templates/index.html'
out_path = 'scratch/get_api_url.txt'

try:
    with open(index_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    matching_lines = []
    for idx, line in enumerate(lines):
        if 'getapiurl' in line.lower() or 'getfetchoptions' in line.lower() or 'api_url' in line.lower():
            matching_lines.append(f"Line {idx+1}: {line.strip()}")
            
    with open(out_path, 'w', encoding='utf-8') as out:
        out.write('\n'.join(matching_lines))
    print("Success")
except Exception as e:
    print(f"Error: {e}")

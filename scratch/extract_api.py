import os

index_path = 'templates/index.html'
out_path = 'scratch/api_calls.txt'

try:
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all strings matching /api/...
    import re
    matches = re.findall(r'[\'"`]/api/[^\'"`]+[\'"`]', content)
            
    with open(out_path, 'w', encoding='utf-8') as out:
        out.write("API calls found in index.html:\n")
        out.write('\n'.join(sorted(list(set(matches)))))
    print("Success")
except Exception as e:
    print(f"Error: {e}")

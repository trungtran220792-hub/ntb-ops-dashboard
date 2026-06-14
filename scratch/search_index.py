import re

def search_in_file(filepath, pattern):
    safe_pattern = pattern.encode('ascii', 'replace').decode('ascii')
    print(f"Searching for '{safe_pattern}' in {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    matches = []
    regex = re.compile(pattern, re.IGNORECASE)
    for i, line in enumerate(lines):
        if regex.search(line):
            matches.append((i+1, line.strip()))
            
    print(f"Found {len(matches)} matches:")
    for num, content in matches[:150]:
        safe_content = content.encode('ascii', 'replace').decode('ascii')
        print(f"Line {num}: {safe_content}")
    if len(matches) > 150:
        print("... truncated ...")

if __name__ == '__main__':
    search_in_file('../templates/index.html', 'suggestion-btn')

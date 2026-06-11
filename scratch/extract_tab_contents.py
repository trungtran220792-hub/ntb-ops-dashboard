import re

def extract_div(filepath, div_id):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        try:
            with open(filepath, 'r', encoding='utf-16') as f:
                content = f.read()
        except Exception as e:
            return f"Error reading file: {e}"

    pattern = rf'(<div[^>]*id=["\']{div_id}["\'][^>]*>)'
    match = re.search(pattern, content)
    if not match:
        return f"Div with id {div_id} not found."
    
    start_pos = match.start()
    open_divs = 0
    pos = start_pos
    while pos < len(content):
        next_tag = re.search(r'</?div\b[^>]*>', content[pos:])
        if not next_tag:
            break
        tag = next_tag.group(0)
        pos += next_tag.start()
        if tag.startswith('</div'):
            open_divs -= 1
            if open_divs == 0:
                end_pos = pos + len(tag)
                return content[start_pos:end_pos]
        else:
            open_divs += 1
        pos += len(tag)
    return "Failed to find matching closing div"

files = {
    "current": "templates/index.html",
    "backup_reset": "scratch/templates_index_backup_before_reset.html",
    "backup_curr": "scratch/index_current_backup.html",
    "head": "scratch/index_head.html",
}

tabs = ["tab-ntb-summary", "tab-volume-creation", "tab-nhan-su"]

for t in tabs:
    print(f"\n==================== TAB: {t} ====================")
    for name, filepath in files.items():
        res = extract_div(filepath, t)
        print(f"File: {name} ({filepath}) | Length: {len(res)} chars")
        if not res.startswith("<div") and len(res) < 100:
            print(f"  Result: {res}")
        else:
            print(f"  Starts with: {res[:80]}")
            print(f"  Ends with: {res[-80:]}")

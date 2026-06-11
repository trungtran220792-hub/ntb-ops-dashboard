import re

def extract_div(filepath, div_id):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Find <div ... id="div_id" ...> to its closing </div>
    # Let's use re with careful tag matching
    pattern = rf'(<div[^>]*id=["\']{div_id}["\'][^>]*>)'
    match = re.search(pattern, content)
    if not match:
        return f"Div with id {div_id} not found."
    
    start_pos = match.start()
    # Find matching closing div
    open_divs = 0
    pos = start_pos
    while pos < len(content):
        # find next tag
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

# Compare tab-volume-creation
v_curr = extract_div("c:/Users/lap4all/Desktop/New folder/templates/index.html", "tab-volume-creation")
v_back = extract_div("c:/Users/lap4all/Desktop/New folder/scratch/templates_index_backup_before_reset.html", "tab-volume-creation")

print(f"=== Volume Creation Tab length ===")
print("Current:", len(v_curr))
print("Backup:", len(v_back))
if v_curr == v_back:
    print("HTML Content is IDENTICAL")
else:
    print("HTML Content is DIFFERENT")

# Compare tab-nhan-su
n_curr = extract_div("c:/Users/lap4all/Desktop/New folder/templates/index.html", "tab-nhan-su")
n_back = extract_div("c:/Users/lap4all/Desktop/New folder/scratch/templates_index_backup_before_reset.html", "tab-nhan-su")

print(f"\n=== Personnel Management Tab length ===")
print("Current:", len(n_curr))
print("Backup:", len(n_back))
if n_curr == n_back:
    print("HTML Content is IDENTICAL")
else:
    print("HTML Content is DIFFERENT")

# Let's also look for JS code differences in the file
with open("c:/Users/lap4all/Desktop/New folder/templates/index.html", 'r', encoding='utf-8') as f:
    js_curr = f.read()
with open("c:/Users/lap4all/Desktop/New folder/scratch/templates_index_backup_before_reset.html", 'r', encoding='utf-8') as f:
    js_back = f.read()

# Let's find script blocks or search for volume/nhan-su specific js functions
print("\n=== JS function checks ===")
for keyword in ["renderVolume", "loadVolume", "NhanSu", "renderUsers", "updateUser", "handleNtbSort", "renderNtbAnalysisTable", "renderNtb", "loadNtb"]:
    in_curr = keyword in js_curr
    in_back = keyword in js_back
    print(f"Keyword '{keyword}': in current={in_curr}, in backup={in_back}")

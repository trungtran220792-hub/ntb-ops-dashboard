import os
import re

def read_file(path):
    if not os.path.exists(path):
        return None
    # Try different encodings
    for enc in ['utf-16', 'utf-8', 'latin1', 'utf-16-le', 'utf-16-be']:
        try:
            with open(path, 'r', encoding=enc) as f:
                content = f.read()
                if len(content) > 10:
                    print(f"Successfully read {path} with {enc}")
                    return content
        except Exception:
            continue
    return None

current = read_file(r"templates/index.html")
base = read_file(r"scratch/index.html.base")
patched = read_file(r"scratch/index.html.patched")

def get_block(content, start_pattern, end_pattern):
    if not content:
        return "No content"
    match = re.search(start_pattern, content)
    if not match:
        return "Start not found"
    start_idx = match.start()
    end_match = re.search(end_pattern, content[start_idx:])
    if not end_match:
        return "End not found"
    return content[start_idx:start_idx + end_match.end()]

def get_js_func(content, func_name):
    if not content:
        return "No content"
    pattern = rf"function\s+{func_name}\s*\("
    match = re.search(pattern, content)
    if not match:
        pattern = rf"const\s+{func_name}\s*=\s*\("
        match = re.search(pattern, content)
        if not match:
            return "Not found"
    
    start_idx = match.start()
    braces = 0
    in_string = False
    string_char = ''
    func_content = []
    for i in range(start_idx, len(content)):
        char = content[i]
        func_content.append(char)
        if not in_string:
            if char in ['"', "'", '`']:
                in_string = True
                string_char = char
            elif char == '{':
                braces += 1
            elif char == '}':
                braces -= 1
                if braces == 0 and len(func_content) > 50:
                    break
        else:
            if char == string_char and content[i-1] != '\\':
                in_string = False
    return "".join(func_content)

# Compare HTML for tab-ntb-summary
print("\n--- tab-ntb-summary in Current vs Base ---")
current_ntb = get_block(current, r'<div[^>]*id="tab-ntb-summary"', r'</div>\s*</div>\s*</div>')
base_ntb = get_block(base, r'<div[^>]*id="tab-ntb-summary"', r'</div>\s*</div>\s*</div>')
print(f"Current length: {len(current_ntb)}, Base length: {len(base_ntb)}")
if current_ntb != base_ntb:
    print("HTML for tab-ntb-summary is DIFFERENT!")
    # Let's write the diff or print first line differences
else:
    print("HTML for tab-ntb-summary is SAME.")

# Compare HTML for tab-opr
print("\n--- tab-opr in Current vs Base ---")
current_opr = get_block(current, r'<div[^>]*id="tab-opr"', r'</div>\s*</div>\s*</div>')
base_opr = get_block(base, r'<div[^>]*id="tab-opr"', r'</div>\s*</div>\s*</div>')
print(f"Current length: {len(current_opr)}, Base length: {len(base_opr)}")
if current_opr != base_opr:
    print("HTML for tab-opr is DIFFERENT!")
else:
    print("HTML for tab-opr is SAME.")

# Let's check some JavaScript functions
for func in ["loadNtbSummaryData", "loadOprDashboardData", "renderOprDashboard", "switchTab"]:
    print(f"\n--- JS Function: {func} ---")
    cf = get_js_func(current, func)
    bf = get_js_func(base, func)
    print(f"Current len: {len(cf)}, Base len: {len(bf)}")
    if cf != bf:
        print(f"Function {func} is DIFFERENT!")
    else:
        print(f"Function {func} is SAME.")

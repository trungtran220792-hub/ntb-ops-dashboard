import difflib
import os

def read_file(path):
    if not os.path.exists(path):
        return None
    for enc in ['utf-16', 'utf-8', 'latin1', 'utf-16-le', 'utf-16-be']:
        try:
            with open(path, 'r', encoding=enc) as f:
                content = f.read()
                if len(content) > 10:
                    return content
        except Exception:
            continue
    return None

current = read_file(r"templates/index.html")
base = read_file(r"scratch/index.html.base")

import re
def get_block(content, start_pattern, end_pattern):
    if not content:
        return ""
    match = re.search(start_pattern, content)
    if not match:
        return ""
    start_idx = match.start()
    end_match = re.search(end_pattern, content[start_idx:])
    if not end_match:
        return ""
    return content[start_idx:start_idx + end_match.end()]

def get_js_func(content, func_name):
    if not content:
        return ""
    pattern = rf"function\s+{func_name}\s*\("
    match = re.search(pattern, content)
    if not match:
        pattern = rf"const\s+{func_name}\s*=\s*\("
        match = re.search(pattern, content)
        if not match:
            return ""
    
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

def show_diff(name, text1, text2):
    lines1 = text1.splitlines(keepends=True)
    lines2 = text2.splitlines(keepends=True)
    diff = list(difflib.unified_diff(lines1, lines2, fromfile='current', tofile='base'))
    return f"\n===== DIFF FOR {name} =====\n" + "".join(diff)

all_diffs = []
all_diffs.append(show_diff("tab-ntb-summary HTML",
                           get_block(current, r'<div[^>]*id="tab-ntb-summary"', r'</div>\s*</div>\s*</div>'),
                           get_block(base, r'<div[^>]*id="tab-ntb-summary"', r'</div>\s*</div>\s*</div>')))

all_diffs.append(show_diff("tab-opr HTML",
                           get_block(current, r'<div[^>]*id="tab-opr"', r'</div>\s*</div>\s*</div>'),
                           get_block(base, r'<div[^>]*id="tab-opr"', r'</div>\s*</div>\s*</div>')))

all_diffs.append(show_diff("loadNtbSummaryData JS",
                           get_js_func(current, "loadNtbSummaryData"),
                           get_js_func(base, "loadNtbSummaryData")))

all_diffs.append(show_diff("renderOprDashboard JS",
                           get_js_func(current, "renderOprDashboard"),
                           get_js_func(base, "renderOprDashboard")))

all_diffs.append(show_diff("switchTab JS",
                           get_js_func(current, "switchTab"),
                           get_js_func(base, "switchTab")))

with open("scratch/print_diffs_res.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(all_diffs))
print("Diff analysis written to scratch/print_diffs_res.txt")

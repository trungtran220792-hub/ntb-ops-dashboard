import re

def run():
    with open("c:/Users/lap4all/Desktop/New folder/templates/index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Find functions containing "Ntb" or related keywords in index.html
    # Let's search for function definitions inside index.html
    funcs = re.findall(r'function\s+([a-zA-Z0-9_]*ntb[a-zA-Z0-9_]*|[a-zA-Z0-9_]*Ntb[a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{', content)
    print("Found NTB functions:", funcs)

    out = []
    # Let's extract the code for these functions plus other potential names
    target_funcs = list(set(funcs + ["loadNtbSummaryData", "updateNtbDashboard", "renderNtbAnalysisTable", "handleNtbSort", "handleNtbSearch", "setNtbGroupType", "switchNtbRegion"]))
    
    for func_name in target_funcs:
        pattern = rf'function\s+{func_name}\s*\([^)]*\)\s*\{{'
        match = re.search(pattern, content)
        if match:
            start_pos = match.start()
            open_brackets = 0
            pos = start_pos
            while pos < len(content):
                if content[pos] == '{':
                    open_brackets += 1
                elif content[pos] == '}':
                    open_brackets -= 1
                    if open_brackets == 0:
                        out.append(f"\n=================== {func_name} ===================")
                        out.append(content[start_pos:pos+1])
                        out.append("====================================================")
                        break
                pos += 1

    with open("c:/Users/lap4all/Desktop/New folder/scratch/ntb_js_code.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))

run()
print("Saved NTB functions to scratch/ntb_js_code.txt")

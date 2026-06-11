import re

filepath = "templates/index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Search for function declarations with 'ntb' or 'Ntb' or 'NTB'
matches = []
for idx, line in enumerate(lines):
    if 'function' in line and any(x in line for x in ['ntb', 'Ntb', 'NTB']):
        matches.append((idx+1, line.strip()))

out_lines = []
for line_num, decl in matches:
    out_lines.append(f"Line {line_num}: {decl}")
    context = lines[line_num:line_num+100]  # get more lines
    out_lines.append("CONTEXT:")
    for c_idx, c_line in enumerate(context):
        out_lines.append(f"  {line_num+c_idx+1}: {c_line.rstrip()}")
    out_lines.append("-" * 50)

with open("scratch/ntb_js_code.txt", "w", encoding="utf-8") as out:
    out.write("\n".join(out_lines))
print("Wrote to scratch/ntb_js_code.txt")

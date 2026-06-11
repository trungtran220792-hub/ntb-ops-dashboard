import re
import difflib

with open("c:/Users/lap4all/Desktop/New folder/scratch/main_script_curr.js", "r", encoding="utf-8") as f:
    curr_lines = f.readlines()

with open("c:/Users/lap4all/Desktop/New folder/scratch/main_script_back.js", "r", encoding="utf-8") as f:
    back_lines = f.readlines()

print(f"Current lines: {len(curr_lines)}, Backup lines: {len(back_lines)}")

# Let's extract functions or look at a line-by-line diff of functions containing "volume" or "user" or "nhan" or "ntb"
curr_js = "".join(curr_lines)
back_js = "".join(back_lines)

# Find function definitions: function foo(...) or const foo = ...
# Or just do a diff of sections
# Let's find all function headers in both
def find_functions(js_text):
    funcs = re.findall(r'(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>)', js_text)
    func_names = sorted(list(set(f[0] or f[1] for f in funcs if f[0] or f[1])))
    return func_names

curr_funcs = find_functions(curr_js)
back_funcs = find_functions(back_js)

print("\nFunctions in current but not in backup:")
print("  ", [f for f in curr_funcs if f not in back_funcs])

print("\nFunctions in backup but not in current:")
print("  ", [f for f in back_funcs if f not in curr_funcs])

# Let's search for "volume" (case insensitive) functions/variables in backup to see if they exist in current
print("\nVolume/Personnel related keywords in current vs backup JS:")
keywords = ["volume", "nhan", "user", "role", "nhansu", "nhan_su", "active_tab", "switchtab"]
for kw in keywords:
    c_count = len(re.findall(kw, curr_js, re.IGNORECASE))
    b_count = len(re.findall(kw, back_js, re.IGNORECASE))
    print(f"Keyword '{kw}': current={c_count}, backup={b_count}")

# Let's perform a diff of the script files
# Since the script files are large, we can output a unified diff of lines that differ
diff = list(difflib.unified_diff(
    curr_lines, 
    back_lines, 
    fromfile="Current Script", 
    tofile="Backup Script",
    n=3
))

print(f"\nUnified diff has {len(diff)} lines.")
# Let's write the diff to scratch
with open("c:/Users/lap4all/Desktop/New folder/scratch/js_diff.txt", "w", encoding="utf-8") as f:
    f.writelines(diff)
print("Saved diff to scratch/js_diff.txt")

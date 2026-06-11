import re

with open("scratch/render_index.html", "r", encoding="utf-8") as f:
    content = f.read()

results = []
def get_block(start_pattern, end_pattern):
    match = re.search(start_pattern, content)
    if not match:
        return "Start not found"
    start_idx = match.start()
    end_match = re.search(end_pattern, content[start_idx:])
    if not end_match:
        return "End not found"
    return content[start_idx:start_idx + end_match.end()]

def check_word(word):
    found = word in content
    results.append(f"Word '{word}': {'FOUND' if found else 'NOT FOUND'}")

results.append("=== CHECKING scratch/render_index.html ===")
check_word("tab-ntb-summary")
check_word("tab-opr")
check_word("opr-overall-rate")
check_word("cachedNtbMatrixData")
check_word("switchNtbRegion")

results.append("\n--- tab-opr HTML snippet ---")
results.append(get_block(r'<div[^>]*id="tab-opr"', r'</div>\s*</div>\s*</div>')[:1000])

results.append("\n--- tab-ntb-summary HTML snippet ---")
results.append(get_block(r'<div[^>]*id="tab-ntb-summary"', r'</div>\s*</div>\s*</div>')[:1000])

with open("scratch/search_render_index_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(results))

print("Render index search done.")

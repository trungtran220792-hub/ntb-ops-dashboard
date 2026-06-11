with open(r"c:\Users\lap4all\Desktop\New folder\scratch\extracted_full_index_changes.txt", 'r', encoding='utf-8') as f:
    content = f.read()

print("File size:", len(content))
if "truncated" in content:
    print("WARNING: File contains the word 'truncated'!")
    # count occurrences
    import re
    truncs = re.findall(r'(<truncated.*?>)', content)
    print("Found truncations:", len(truncs))
    for t in truncs[:5]:
        print("  Truncation tag:", t)
else:
    print("Nice! File does not contain any truncation words.")

# Let's search for overall kpi card replacements
match = re.search(r'Báo Cáo Hiệu Suất OPR TTS.*?(?=== STEP|=== CHUNKS|$)', content, re.DOTALL)
if match:
    print("Found OPR section in changes!")
    print("Length of section:", len(match.group(0)))
    with open(r"c:\Users\lap4all\Desktop\New folder\scratch\opr_section_found.txt", 'w', encoding='utf-8') as out:
        out.write(match.group(0))
else:
    print("OPR section not found.")

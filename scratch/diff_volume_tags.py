def search_and_get(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    import re
    matches = re.findall(r'<[^>]+(?:id|class|onclick|href)=[^>]*(?:volume|tao-don)[^>]*>', content, re.IGNORECASE)
    return [m.strip() for m in matches]

curr = search_and_get("c:/Users/lap4all/Desktop/New folder/templates/index.html")
back = search_and_get("c:/Users/lap4all/Desktop/New folder/scratch/templates_index_backup_before_reset.html")

print("Tags in BACKUP but not in CURRENT:")
for b in back:
    if b not in curr:
        print("  ", b)

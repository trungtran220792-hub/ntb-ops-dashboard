def search_and_print(filepath, label):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    import re
    # Find all IDs or classes or tags containing volume or tao-don
    matches = re.findall(r'<[^>]+(?:id|class|onclick|href)=[^>]*(?:volume|tao-don)[^>]*>', content, re.IGNORECASE)
    print(f"=== {label} volume tags: {len(matches)} ===")
    for m in matches[:15]:
        print("  ", m.strip())

search_and_print("c:/Users/lap4all/Desktop/New folder/templates/index.html", "CURRENT")
search_and_print("c:/Users/lap4all/Desktop/New folder/scratch/templates_index_backup_before_reset.html", "BACKUP")

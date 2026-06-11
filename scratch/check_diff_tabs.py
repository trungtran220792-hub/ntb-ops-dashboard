import re

def parse_sidebar_and_panels(filepath):
    print(f"=== Parsing {filepath} ===")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Let's find sidebar links
    # Typically looks like <a ... href="#" data-tab="..." or similar
    links = re.findall(r'<a[^>]+(?:class|id)=[^>]+>[^<]*<\/a>', content)
    print("Found links:")
    for l in links[:30]:
        if 'tab' in l.lower() or 'active' in l.lower() or 'nhân sự' in l.lower() or 'đơn' in l.lower() or 'ntb' in l.lower() or 'opr' in l.lower():
            print("  ", l.strip())

    # Let's find IDs matching tab-* or panel-* or sections
    ids = re.findall(r'id=["\']([^"\']+)["\']', content)
    tab_ids = [i for i in ids if 'tab' in i.lower() or 'panel' in i.lower()]
    print("Tab/Panel related IDs:")
    print("  ", tab_ids)

parse_sidebar_and_panels("c:/Users/lap4all/Desktop/New folder/templates/index.html")
parse_sidebar_and_panels("c:/Users/lap4all/Desktop/New folder/scratch/templates_index_backup_before_reset.html")

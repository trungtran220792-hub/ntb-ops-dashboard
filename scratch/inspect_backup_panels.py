# -*- coding: utf-8 -*-
import os

backup_path = r"c:\Users\lap4all\Desktop\New folder\scratch\templates_index_backup_before_reset.html"
with open(backup_path, "r", encoding="utf-8") as f:
    content = f.read()

# Let's extract the div with id="tab-nhan-su"
start_str = '<div id="tab-nhan-su" class="content-panel">'
idx = content.find(start_str)

if idx != -1:
    # Find matching closing div or just extract until the next panel: "<!-- TAB: ... -->" or "<!-- TAB 1: ... -->"
    # Or simply extract until the next `<div id="tab-...` or similar.
    # Let's see what is the next div. The next panel is likely <div id="tab-sync" or similar.
    next_idx = content.find('<div id="tab-sync"', idx + len(start_str))
    if next_idx == -1:
        # fallback
        next_idx = idx + 10000
    
    panel_content = content[idx:next_idx]
    
    with open(r"scratch\nhan_su_panel.html", "w", encoding="utf-8") as out:
        out.write(panel_content)
    print(f"Extracted nhan_su_panel.html, size={len(panel_content)} chars")
else:
    print("tab-nhan-su not found")

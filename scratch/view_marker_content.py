with open("c:/Users/lap4all/Desktop/New folder/templates/index.html", "r", encoding="utf-8") as f:
    text = f.read()

start_kw = '        // ==========================================\n        // NTB SUMMARY DASHBOARD TAB LOGIC'
end_kw = '        /* ==========================================================================\n           GHN AI CHAT LOGIC'

start_idx = text.find(start_kw)
end_idx = text.find(end_kw)

if start_idx != -1 and end_idx != -1:
    section_content = text[start_idx:end_idx]
    with open("c:/Users/lap4all/Desktop/New folder/scratch/current_marker_content.txt", "w", encoding="utf-8") as f:
        f.write(section_content)
    print("Saved current content to scratch/current_marker_content.txt, length:", len(section_content))
else:
    print("Markers not found.")

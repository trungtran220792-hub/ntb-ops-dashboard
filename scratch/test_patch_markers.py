with open("c:/Users/lap4all/Desktop/New folder/templates/index.html", "r", encoding="utf-8") as f:
    text = f.read()

start_kw = '        // ==========================================\n        // NTB SUMMARY DASHBOARD TAB LOGIC'
end_kw = '        /* ==========================================================================\n           GHN AI CHAT LOGIC'

start_idx = text.find(start_kw)
end_idx = text.find(end_kw)

print(f"Start index: {start_idx}")
print(f"End index: {end_idx}")

if start_idx != -1 and end_idx != -1:
    print("Markers exist! We can run the patch.")
else:
    # Try case-insensitive or looser search
    print("Checking loose search...")
    for marker in ['NTB SUMMARY DASHBOARD', 'GHN AI CHAT LOGIC']:
        idx = text.lower().find(marker.lower())
        print(f"Marker '{marker}': index={idx}")

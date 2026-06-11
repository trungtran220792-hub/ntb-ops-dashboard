with open(r"c:\Users\lap4all\Desktop\New folder\scratch\templates_index_backup_before_reset.html", 'r', encoding='utf-8') as f:
    content = f.read()

# Look for tab-opr
import re
match_html = re.search(r'(<!-- TAB 3: OPR TTS -->.*?<!-- TAB 4: BACKLOG)', content, re.DOTALL)
if match_html:
    print("Found tab-opr HTML in backup!")
    with open(r"c:\Users\lap4all\Desktop\New folder\scratch\recovered_tab_opr_html.html", 'w', encoding='utf-8') as out:
        out.write(match_html.group(1))
    print("Saved HTML to scratch/recovered_tab_opr_html.html")
else:
    print("Could not find tab-opr HTML block in backup.")

# Look for OPR script functions
match_js = re.search(r'(// ==========================================\s*// RENDER: OPR TTS DASHBOARD.*?// ==========================================\s*// RENDER: BACKLOG)', content, re.DOTALL)
if match_js:
    print("Found tab-opr JS functions in backup!")
    with open(r"c:\Users\lap4all\Desktop\New folder\scratch\recovered_tab_opr_js.js", 'w', encoding='utf-8') as out:
        out.write(match_js.group(1))
    print("Saved JS to scratch/recovered_tab_opr_js.js")
else:
    # Try looking for renderOprDashboard
    match_js_alt = re.search(r'(function renderOprDashboard.*?function renderAgingDashboard)', content, re.DOTALL)
    if match_js_alt:
        print("Found renderOprDashboard in backup (alternative search)!")
        with open(r"c:\Users\lap4all\Desktop\New folder\scratch\recovered_tab_opr_js.js", 'w', encoding='utf-8') as out:
            out.write(match_js_alt.group(1))
        print("Saved JS to scratch/recovered_tab_opr_js.js")
    else:
        print("Could not find OPR JS functions in backup.")

# -*- coding: utf-8 -*-
import os

scratch_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"
files = ["index_changes_ntb.txt", "index_changes_ntb_formatted.txt", "extracted_ntb_js_from_summary.txt", "tab_ntb_js_current.txt", "tab_ntb_js_current_part2.txt", "script_opr_funcs.txt"]

for filename in files:
    path = os.path.join(scratch_dir, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        print(f"File: {filename}, size: {len(content)} chars")
        # Check occurrences of renderNtbAnalysisTable
        count = content.count("renderNtbAnalysisTable")
        print(f"  renderNtbAnalysisTable occurrences: {count}")
        # Let's search if any definition doesn't have '<truncated' in the surrounding 2000 chars
        idx = 0
        while True:
            idx = content.find("function renderNtbAnalysisTable", idx)
            if idx == -1:
                break
            snippet = content[idx:idx+3000]
            has_truncation = "truncated" in snippet or "..." in snippet and len(snippet) < 3000
            print(f"  Definition at char {idx}: has_truncation={has_truncation}")
            if not has_truncation:
                print("  Found complete definition! Writing snippet to file...")
                with open(os.path.join(scratch_dir, f"found_complete_{filename}.txt"), "w", encoding="utf-8") as f_out:
                    f_out.write(content[idx:idx+8000]) # write a large chunk
            idx += 1

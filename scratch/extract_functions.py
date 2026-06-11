# -*- coding: utf-8 -*-
import os
import re

scratch_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"
log_file = os.path.join(scratch_dir, "past_ntb_funcs_found.txt")

with open(log_file, "r", encoding="utf-8") as f:
    content = f.read()

# Let's search for blocks starting with "--- REPLACEMENT CONTENT ---" or similar
# or just grep for functions in this log file and print their definitions.
print("Total length of log file:", len(content))

queries = ["renderNtbAnalysisTable", "setAmOprSort", "renderNtbKpiCards", "switchNtbRegion", "renderOprDashboard", "setNtbGroupType", "handleNtbSearch", "handleNtbSort"]

with open(os.path.join(scratch_dir, "extracted_snippets.txt"), "w", encoding="utf-8") as out:
    out.write(f"Total length of log file: {len(content)}\n\n")

    for q in queries:
        occurrences = [m.start() for m in re.finditer(q, content)]
        out.write(f"Found {len(occurrences)} occurrences of '{q}'\n")
        if occurrences:
            # write snippet of occurrences
            for count, idx in enumerate(occurrences[:3]):  # get up to 3 occurrences
                start = max(0, idx - 400)
                end = min(len(content), idx + 4000)
                out.write(f"--- Occurrence {count+1} of {q} ---\n")
                out.write(content[start:end])
                out.write("\n" + "="*80 + "\n\n")
print("Done writing to extracted_snippets.txt")

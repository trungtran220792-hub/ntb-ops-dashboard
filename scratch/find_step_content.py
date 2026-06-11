# -*- coding: utf-8 -*-
import os
import re

scratch_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"
log_file = os.path.join(scratch_dir, "past_ntb_funcs_found.txt")

with open(log_file, "r", encoding="utf-8") as f:
    content = f.read()

# Let's find steps and extract their full replacement content.
# The format seems to be:
# CONV: ... - STEP <step_num> - TOOL: replace_file_content
# ...
# --- TARGET CONTENT ---
# ...
# --- REPLACEMENT CONTENT ---
# ...
# ========================================

steps = re.findall(r"STEP\s+(\d+)", content)
print("Steps found in log file:", sorted(list(set(steps))))

# Let's search for step 147, 593, 1155, 1157, 1167, 1171, 1177, 157, 544
target_steps = ["147", "593", "1155", "1157", "1167", "1171", "1177", "157", "544"]

with open(os.path.join(scratch_dir, "step_details_extracted.txt"), "w", encoding="utf-8") as out:
    for ts in target_steps:
        # Find all occurrences of "STEP ts"
        pattern = r"(CONV:[^\n]*STEP\s+" + ts + r"\b.*?)(?===+|$)"
        matches = re.findall(pattern, content, re.DOTALL)
        out.write(f"=== STEP {ts} matches found: {len(matches)} ===\n\n")
        for idx, m in enumerate(matches):
            out.write(f"--- MATCH {idx+1} for STEP {ts} ---\n")
            out.write(m)
            out.write("\n" + "="*80 + "\n\n")

print("Done writing step details to step_details_extracted.txt")

# -*- coding: utf-8 -*-
import os

scratch_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"
log_file = os.path.join(scratch_dir, "past_ntb_funcs_found.txt")

with open(log_file, "r", encoding="utf-8") as f:
    content = f.read()

blocks = content.split("========================================")
print("Total blocks found:", len(blocks))

target_steps = ["147", "593", "1155", "1157", "1167", "1171", "1177", "157", "544"]

with open(os.path.join(scratch_dir, "step_blocks_extracted.txt"), "w", encoding="utf-8") as out:
    for block in blocks:
        # Check if this block matches any target step
        # Look for "STEP <num>" as a word
        for ts in target_steps:
            if f"STEP {ts}" in block or f"STEP  {ts}" in block:
                out.write("========================================\n")
                out.write(block)
                out.write("\n========================================\n\n")

print("Done writing blocks to step_blocks_extracted.txt")

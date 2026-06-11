# -*- coding: utf-8 -*-
import os

scratch_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"
log_file = os.path.join(scratch_dir, "past_ntb_funcs_found.txt")

with open(log_file, "r", encoding="utf-8") as f:
    content = f.read()

# Let's search for "updateMetricCardUI" and print around it
with open(os.path.join(scratch_dir, "search_kpis_js_res.txt"), "w", encoding="utf-8") as out:
    idx = 0
    while True:
        idx = content.find("updateMetricCardUI", idx)
        if idx == -1:
            break
        out.write(f"Found updateMetricCardUI at character: {idx}\n")
        snippet = content[idx - 200 : idx + 3000]
        out.write("--- SNIPPET ---\n")
        out.write(snippet)
        out.write("\n" + "="*80 + "\n\n")
        idx += len("updateMetricCardUI")
print("Done writing to search_kpis_js_res.txt")

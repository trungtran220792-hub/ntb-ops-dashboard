# -*- coding: utf-8 -*-
import os

backup_path = r"c:\Users\lap4all\Desktop\New folder\scratch\templates_index_backup_before_reset.html"
with open(backup_path, "r", encoding="utf-8") as f:
    content = f.read()

# Let's extract sendTelegramAiBriefing, sendTelegramWarning, and the nhan su js functions.
# They are located inside the script tag.
# We can find them by searching for "async function sendTelegramAiBriefing"
idx_ai = content.find("async function sendTelegramAiBriefing")
idx_warn = content.find("async function sendTelegramWarning")
idx_ns = content.find("// ==========================================\n        // RENDER: NHÂN SỰ & SCENARIO PLANNER (TAB)")

with open(r"scratch\backup_js_functions.js", "w", encoding="utf-8") as out:
    if idx_ai != -1:
        out.write("=== sendTelegramAiBriefing ===\n")
        # Extract until the next function
        next_fn = content.find("async function sendTelegramWarning", idx_ai)
        out.write(content[idx_ai:next_fn])
        out.write("\n\n")
    if idx_warn != -1:
        out.write("=== sendTelegramWarning ===\n")
        # Extract until the next function, which might be showLoading or similar
        next_fn = content.find("function showLoading", idx_warn)
        out.write(content[idx_warn:next_fn])
        out.write("\n\n")
    if idx_ns != -1:
        out.write("=== NHAN SU JS ===\n")
        # Extract until the end of the script tag (usually before </script>)
        next_fn = content.find("</script>", idx_ns)
        out.write(content[idx_ns:next_fn])
        out.write("\n\n")

print("Done extracting JS functions")

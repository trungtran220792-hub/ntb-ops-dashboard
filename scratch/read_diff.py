with open(r"scratch\diff_app_full.txt", "r", encoding="utf-8") as f:
    app_diff = f.read()

with open(r"scratch\diff_index.txt", "r", encoding="utf-8") as f:
    index_diff = f.read()

print("App diff length:", len(app_diff))
print("Index diff length:", len(index_diff))

# Let's see if the output is truncated (contains "<truncated" or similar)
if "truncated" in app_diff.lower() or "truncated" in index_diff.lower():
    print("WARNING: Diffs are truncated in the log!")
    if "truncated" in app_diff.lower():
        print("App diff has truncation")
    if "truncated" in index_diff.lower():
        print("Index diff has truncation")
else:
    print("Excellent! Diffs are NOT truncated!")

with open("templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()

features = [
    "opr-overall-rate",
    "sort-am-asc",
    "table-opr-errors",
    "cachedNtbMatrixData",
    "switchNtbRegion",
    "renderNtbKpiCards",
    "loadOprData",
    "setAmOprSort",
    "renderOprAmChartOnly"
]

results = []
for feat in features:
    found = feat in content
    results.append(f"Feature '{feat}': {'FOUND' if found else 'NOT FOUND'}")

with open("scratch/check_features_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(results))

print("Feature check done.")

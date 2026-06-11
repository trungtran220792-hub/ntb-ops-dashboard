with open("c:/Users/lap4all/Desktop/New folder/templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
out = []

pattern = r'renderVolumeCreation\s*\('
matches = [m.start() for m in re.finditer(pattern, content)]
out.append("renderVolumeCreation calls:")
for idx in matches:
    out.append(content[max(0, idx - 100):min(len(content), idx + 200)])
    out.append("-" * 50)

out.append("\nFilter change handlers / load calls for volume:")
lines = content.splitlines()
for i, line in enumerate(lines):
    if "vol-" in line or "volume" in line.lower() or "tao-don" in line.lower():
        if "function " in line or "onchange=" in line or "onclick=" in line or "oninput=" in line:
            out.append(f"L{i+1}: {line.strip()}")

with open("c:/Users/lap4all/Desktop/New folder/scratch/volume_calls_results.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("Saved results to scratch/volume_calls_results.txt")

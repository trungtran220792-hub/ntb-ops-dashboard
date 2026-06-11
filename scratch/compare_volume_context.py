import re

def compare():
    with open("c:/Users/lap4all/Desktop/New folder/scratch/main_script_curr.js", "r", encoding="utf-8") as f:
        curr_js = f.read()

    with open("c:/Users/lap4all/Desktop/New folder/scratch/main_script_back.js", "r", encoding="utf-8") as f:
        back_js = f.read()

    output = []
    
    def find_context(js_text, keyword, label):
        output.append(f"\n=================== {label} ===================")
        matches = [m.start() for m in re.finditer(keyword, js_text)]
        output.append(f"Matches count: {len(matches)}")
        for idx in matches:
            start = max(0, idx - 150)
            end = min(len(js_text), idx + 800)
            output.append(f"\n--- Context at index {idx} ---")
            output.append(js_text[start:end])
            output.append("-" * 30)

    find_context(curr_js, "volume-creation", "CURRENT")
    find_context(back_js, "volume-creation", "BACKUP")

    with open("c:/Users/lap4all/Desktop/New folder/scratch/volume_context_comparison.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output))

compare()
print("Saved comparison to scratch/volume_context_comparison.txt")

import json
import os

path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\2742477c-f9ad-4ec9-923d-4fdf4f5c14ba\.system_generated\logs\transcript.jsonl"
changes = []

with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            step = json.loads(line)
            step_idx = step.get("step_index", 0)
            tool_calls = step.get("tool_calls")
            if tool_calls:
                for tc in tool_calls:
                    func = tc.get("function", {})
                    name = func.get("name")
                    if name in ["replace_file_content", "multi_replace_file_content", "write_to_file"]:
                        args = func.get("arguments", {})
                        target = args.get("TargetFile", "")
                        if "index.html" in target:
                            changes.append({
                                "step": step_idx,
                                "tool": name,
                                "instruction": args.get("Instruction") or args.get("Description", "No description"),
                                "args": args
                            })
        except Exception:
            pass

with open("scratch/index_changes_history.json", "w", encoding="utf-8") as out:
    json.dump(changes, out, indent=2, ensure_ascii=False)

print(f"Extracted {len(changes)} changes to scratch/index_changes_history.json")

import json

path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\2742477c-f9ad-4ec9-923d-4fdf4f5c14ba\.system_generated\logs\transcript.jsonl"
events = []

with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            step = json.loads(line)
            step_idx = step.get("step_index", 0)
            if 1150 <= step_idx <= 1250:
                events.append(f"\n=========================================\nStep {step_idx} | Type: {step.get('type')} | Source: {step.get('source')}")
                if "content" in step and step["content"]:
                    events.append(f"Content: {step['content'][:400]}")
                if "tool_calls" in step:
                    for tc in step["tool_calls"]:
                        func = tc.get("function", {})
                        args = func.get("arguments", {})
                        args_str = str(args)
                        if len(args_str) > 500:
                            args_str = args_str[:500] + "... TRUNCATED ..."
                        events.append(f"Tool call: {func.get('name')} -> {args_str}")
        except Exception:
            pass

with open("scratch/scan_steps_1150_1250.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(events))

print(f"Saved {len(events)} events to scratch/scan_steps_1150_1250.txt")

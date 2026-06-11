import json

transcript_path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\2742477c-f9ad-4ec9-923d-4fdf4f5c14ba\.system_generated\logs\transcript.jsonl"
out_path = r"c:\Users\lap4all\Desktop\New folder\scratch\found_tool_calls.txt"

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            step = json.loads(line)
            idx = step.get("step_index")
            if 1190 <= idx <= 1220:
                tool_calls = step.get("tool_calls", [])
                if tool_calls:
                    for tc in tool_calls:
                        if "replace_file_content" in tc.get("name", ""):
                            print(f"Found replace_file_content at step {idx}")
                            with open(out_path, 'w', encoding='utf-8') as out_f:
                                out_f.write(json.dumps(tc, indent=2, ensure_ascii=False))
                            print(f"Dumped step {idx} to {out_path}")
        except Exception as e:
            pass

import json

transcript_path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\2742477c-f9ad-4ec9-923d-4fdf4f5c14ba\.system_generated\logs\transcript.jsonl"
out_path = r"c:\Users\lap4all\Desktop\New folder\scratch\step_1200_replacement.txt"

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            step = json.loads(line)
            if step.get("step_index") == 1200:
                tool_calls = step.get("tool_calls", [])
                for tc in tool_calls:
                    if tc.get("name") == "replace_file_content":
                        args = tc.get("arguments", {})
                        repl = args.get("ReplacementContent", "")
                        with open(out_path, 'w', encoding='utf-8') as out_f:
                            out_f.write(repl)
                        print("Successfully extracted ReplacementContent!")
                        break
        except Exception as e:
            pass

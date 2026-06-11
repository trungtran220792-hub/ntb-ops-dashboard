import json

transcript_path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\2742477c-f9ad-4ec9-923d-4fdf4f5c14ba\.system_generated\logs\transcript.jsonl"

def extract_step(step_idx, filename):
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                step = json.loads(line)
                if step.get("step_index") == step_idx:
                    for tc in step.get("tool_calls", []):
                        if "replace_file_content" in tc.get("name", ""):
                            args = tc.get("args", {})
                            repl = args.get("ReplacementContent", "")
                            
                            # Decapsulate JSON string if it is double-serialized
                            if repl.startswith('"') and repl.endswith('"'):
                                repl = json.loads(repl)
                            
                            with open(filename, 'w', encoding='utf-8') as out_f:
                                out_f.write(repl)
                            print(f"Extracted step {step_idx} to {filename}")
                            return
            except Exception as e:
                import traceback
                traceback.print_exc()

extract_step(1199, r"c:\Users\lap4all\Desktop\New folder\scratch\step_1199_replacement.txt")
extract_step(1211, r"c:\Users\lap4all\Desktop\New folder\scratch\step_1211_replacement.txt")
print("Done!")

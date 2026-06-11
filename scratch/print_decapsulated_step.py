import json

transcript_path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\2742477c-f9ad-4ec9-923d-4fdf4f5c14ba\.system_generated\logs\transcript.jsonl"

def dump_decrypted(step_idx, filename):
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                step = json.loads(line)
                if step.get("step_index") == step_idx:
                    for tc in step.get("tool_calls", []):
                        if "replace_file_content" in tc.get("name", ""):
                            args = tc.get("args", {})
                            repl = args.get("ReplacementContent", "")
                            
                            # Keep decoding until it doesn't look like a JSON-serialized string
                            while (isinstance(repl, str) and 
                                   ((repl.startswith('"') and repl.endswith('"')) or 
                                    (repl.startswith('{') and repl.endswith('}')) or
                                    (repl.startswith('[') and repl.endswith(']')))):
                                try:
                                    repl = json.loads(repl)
                                except:
                                    break
                            
                            with open(filename, 'w', encoding='utf-8') as out_f:
                                out_f.write(repl)
                            print(f"Decoded and saved step {step_idx} to {filename}")
                            return
            except Exception as e:
                pass

dump_decrypted(1199, r"c:\Users\lap4all\Desktop\New folder\scratch\step_1199_clean.txt")
dump_decrypted(1211, r"c:\Users\lap4all\Desktop\New folder\scratch\step_1211_clean.txt")
print("Done!")

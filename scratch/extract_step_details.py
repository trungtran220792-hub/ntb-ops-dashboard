import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\0d711590-0357-43ee-a937-04cabf62a0ba\.system_generated\logs\transcript.jsonl"

if os.path.exists(path):
    print("Log file exists! Extracting full contents...")
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                step = data.get("step_index")
                if step in [544, 157, 73]:
                    print(f"Extracting step {step}...")
                    for tc in data.get("tool_calls", []):
                        if tc.get("name") in ["replace_file_content", "write_to_file", "multi_replace_file_content"]:
                            args = tc.get("args", {})
                            repl_content = args.get("ReplacementContent", "")
                            target_content = args.get("TargetContent", "")
                            
                            with open(f"scratch/step_{step}_repl.txt", "w", encoding="utf-8") as out:
                                out.write(repl_content)
                            with open(f"scratch/step_{step}_target.txt", "w", encoding="utf-8") as out:
                                out.write(target_content)
                            print(f"  Wrote step_{step}_repl.txt and step_{step}_target.txt")
            except Exception as e:
                print(f"Error on line: {e}")
else:
    print("Log file does not exist at " + path)

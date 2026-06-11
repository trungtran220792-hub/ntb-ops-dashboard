import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\4336314d-71dd-4e55-8828-c64201e3d4a3\.system_generated\logs\transcript.jsonl"

if os.path.exists(path):
    print("Found transcript. Scanning Step 2097...")
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                step = data.get("step_index")
                if step == 2097:
                    print(f"=== Step {step} ===")
                    tool_calls = data.get("tool_calls", [])
                    for tc in tool_calls:
                        args = tc.get("args", {})
                        repl = args.get("ReplacementContent", "")
                        target = args.get("TargetContent", "")
                        
                        print(f"Replacement Content Length: {len(repl)}")
                        print(f"Target Content Length: {len(target)}")
                        
                        # Write to scratch files
                        with open("scratch/step_2097_repl.txt", "w", encoding="utf-8") as out:
                            out.write(repl)
                        with open("scratch/step_2097_target.txt", "w", encoding="utf-8") as out:
                            out.write(target)
                        print("Saved replacement content to scratch/step_2097_repl.txt")
            except Exception as e:
                print(e)
else:
    print("Transcript not found.")

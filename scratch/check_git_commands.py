import os
import json

brain_dir = r"C:\Users\lap4all\.gemini\antigravity-ide\brain"
cid = "0d711590-0357-43ee-a937-04cabf62a0ba"
tpath = os.path.join(brain_dir, cid, ".system_generated", "logs", "transcript.jsonl")

if os.path.exists(tpath):
    with open(tpath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if "git" in line.lower() and "run_command" in line:
                data = json.loads(line)
                step = data.get('step_index')
                for tc in data.get('tool_calls', []):
                    args = tc.get('args', {})
                    cmd = args.get('CommandLine', '')
                    if "git" in cmd:
                        print(f"Step {step}: {cmd}")
else:
    print("Log not found.")

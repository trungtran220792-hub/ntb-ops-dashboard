import json
import os

target_conv_id = "0d711590-0357-43ee-a937-04cabf62a0ba"
transcript_path = fr"C:\Users\lap4all\.gemini\antigravity-ide\brain\{target_conv_id}\.system_generated\logs\transcript.jsonl"

if not os.path.exists(transcript_path):
    print("Transcript not found")
    exit(1)

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            step_idx = data.get('step_index')
            if step_idx >= 930:
                print(f"--- STEP {step_idx} ({data.get('type')}, {data.get('source')}) ---")
                if 'thinking' in data and data['thinking']:
                    print("Thinking:", data['thinking'][:300].strip())
                if 'tool_calls' in data and data['tool_calls']:
                    print("Tool Calls:")
                    for tc in data['tool_calls']:
                        print(f"  Name: {tc.get('name')}")
                        args = tc.get('args', {})
                        # print some key args
                        for k in ['CommandLine', 'TargetFile', 'Description', 'Instruction', 'Url']:
                            if k in args:
                                print(f"    {k}: {args[k][:200]}")
                if 'content' in data and data['content'] and data.get('type') == 'RUN_COMMAND':
                    print("Output:", data['content'][:300].strip())
                print()
        except Exception as e:
            pass

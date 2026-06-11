import json
import os

target_conv_id = "0d711590-0357-43ee-a937-04cabf62a0ba"
transcript_path = fr"C:\Users\lap4all\.gemini\antigravity-ide\brain\{target_conv_id}\.system_generated\logs\transcript.jsonl"

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            step_idx = data.get('step_index')
            if 940 <= step_idx <= 965:
                print(f"--- STEP {step_idx} ({data.get('type')}, {data.get('source')}) ---")
                if 'thinking' in data and data['thinking']:
                    print("Thinking:", data['thinking'].strip())
                if 'tool_calls' in data and data['tool_calls']:
                    print("Tool Calls:")
                    for tc in data['tool_calls']:
                        print(f"  Name: {tc.get('name')}")
                        print(f"    Args: {json.dumps(tc.get('args'), ensure_ascii=False)}")
                if 'content' in data and data['content']:
                    print("Content/Output:", data['content'].strip()[:500])
                print("="*60 + "\n")
        except Exception as e:
            pass

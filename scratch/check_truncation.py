import os
import json

transcript_path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\0d711590-0357-43ee-a937-04cabf62a0ba\.system_generated\logs\transcript.jsonl"
if os.path.exists(transcript_path):
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                step = data.get('step_index')
                if step in [64, 73, 157, 544]:
                    print(f"Step {step}:")
                    for tc in data.get('tool_calls', []):
                        args = tc.get('args', {})
                        for k, v in args.items():
                            if isinstance(v, str) and len(v) > 100:
                                print(f"  {k} (len={len(v)}): {repr(v[:150])}")
                                if "truncated" in v.lower():
                                    print("    WARNING: contains 'truncated'")
            except Exception as e:
                pass
else:
    print("Log not found")

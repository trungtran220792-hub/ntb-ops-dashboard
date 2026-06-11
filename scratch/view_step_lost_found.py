# -*- coding: utf-8 -*-
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

transcript_path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\0d711590-0357-43ee-a937-04cabf62a0ba\.system_generated\logs\transcript.jsonl"

if os.path.exists(transcript_path):
    print("Found transcript. Scanning steps...")
    with open(transcript_path, 'r', encoding='utf-8', errors='ignore') as f:
        for idx, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                step = data.get('step_index')
                if step and 940 <= step <= 955:
                    print(f"\n=== Step {step} | Type {data.get('type')} ===")
                    tool_calls = data.get('tool_calls', [])
                    for tc in tool_calls:
                        print(f"  Tool: {tc.get('name')}")
                        print(f"  Args: {json.dumps(tc.get('args'))[:200]}")
                    content = data.get('content', '')
                    if content:
                        print(f"  Content: {content[:200]}")
            except Exception as e:
                pass
else:
    print("Transcript not found.")

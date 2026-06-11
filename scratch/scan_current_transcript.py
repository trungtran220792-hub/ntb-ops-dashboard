# -*- coding: utf-8 -*-
import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

transcript_path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\2742477c-f9ad-4ec9-923d-4fdf4f5c14ba\.system_generated\logs\transcript.jsonl"
res_path = r"c:\Users\lap4all\Desktop\New folder\scratch\scan_transcript_res.txt"

if os.path.exists(transcript_path):
    print(f"Scanning {transcript_path}...")
    events = []
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f):
            try:
                step = json.loads(line)
            except Exception as e:
                continue
            
            step_idx = step.get("step_index", line_num)
            if 1746 <= step_idx <= 2050:
                events.append(f"\n=========================================\nStep {step_idx} | Type: {step.get('type')} | Source: {step.get('source')}")
                if "content" in step and step["content"]:
                    events.append(f"Content: {step['content'][:500]}")
                if "tool_calls" in step:
                    for tc in step["tool_calls"]:
                        func = tc.get("function", {})
                        events.append(f"Tool call: {func.get('name')} -> {func.get('arguments')}")
                
    with open(res_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(events))
    print(f"Saved {len(events)} events to scan_transcript_res.txt")
else:
    print("Transcript not found")

import json
import os

log_file = r'C:\Users\lap4all\.gemini\antigravity-ide\brain\0d711590-0357-43ee-a937-04cabf62a0ba\.system_generated\logs\transcript.jsonl'

if os.path.exists(log_file):
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                step = data.get('step_index')
                t = data.get('type')
                st = data.get('status')
                tc = data.get('tool_calls')
                if tc:
                    tools = [x.get('name') for x in tc]
                    print(f"Step {step}: type={t}, status={st}, tools={tools}")
                elif t == 'TOOL_RESPONSE':
                    print(f"Step {step}: type={t}, status={st}")
            except Exception as e:
                pass

import json
import os

log_file = r'C:\Users\lap4all\.gemini\antigravity-ide\brain\0d711590-0357-43ee-a937-04cabf62a0ba\.system_generated\logs\transcript.jsonl'

if not os.path.exists(log_file):
    print("Log file not found.")
else:
    print("Reading log file...")
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get('type') == 'TOOL_RESPONSE' or 'console' in str(data).lower():
                    # Check if console logs were returned
                    content = str(data.get('content', ''))
                    if 'console' in content.lower() or 'error' in content.lower():
                        print(f"Step {data.get('step_index')}: {content[:300]}")
            except Exception as e:
                pass

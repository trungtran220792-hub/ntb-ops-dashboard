import json
import pprint

tpath = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\92726133-7314-4954-9f94-c885d0c26df2\.system_generated\logs\transcript.jsonl"
with open(tpath, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        if data.get('step_index') == 115:
            pprint.pprint(data)
            break

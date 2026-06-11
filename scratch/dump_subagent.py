import json
import os

log_file = r'C:\Users\lap4all\.gemini\antigravity-ide\brain\0d711590-0357-43ee-a937-04cabf62a0ba\.system_generated\logs\transcript.jsonl'

if os.path.exists(log_file):
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                step = data.get('step_index')
                if step == 386:
                    with open(r'c:\Users\lap4all\Desktop\New folder\scratch\subagent_details.txt', 'w', encoding='utf-8') as f_out:
                        f_out.write(json.dumps(data, indent=2, ensure_ascii=False))
                    print("Dumped step 386 to scratch/subagent_details.txt")
                    break
            except Exception as e:
                pass

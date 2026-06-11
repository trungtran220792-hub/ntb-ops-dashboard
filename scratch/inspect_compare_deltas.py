import json

tpath = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\92726133-7314-4954-9f94-c885d0c26df2\.system_generated\logs\transcript.jsonl"
with open(tpath, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        step = data.get('step_index')
        if step == 123:
            tc = data['tool_calls'][0]
            args = tc['args']
            target = args.get('TargetContent', '')
            print("Target type:", type(target))
            print("First 10 chars of target:", list(target[:10]))
            print("Last 10 chars of target:", list(target[-10:]))
            break

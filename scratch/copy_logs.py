import json

tpath = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\4336314d-71dd-4e55-8828-c64201e3d4a3\.system_generated\logs\transcript.jsonl"

step_13_content = None
step_15_content = None

with open(tpath, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            step = data.get('step_index')
            if step == 13:
                step_13_content = data.get('content')
            elif step == 15:
                step_15_content = data.get('content')
        except Exception as e:
            pass

if step_13_content:
    with open(r"c:\Users\lap4all\Desktop\New folder\scratch\diff_app_full.txt", "w", encoding="utf-8") as f:
        f.write(step_13_content)
    print("Wrote diff_app_full.txt")
else:
    print("Step 13 content not found")

if step_15_content:
    with open(r"c:\Users\lap4all\Desktop\New folder\scratch\diff_index.txt", "w", encoding="utf-8") as f:
        f.write(step_15_content)
    print("Wrote diff_index.txt")
else:
    print("Step 15 content not found")

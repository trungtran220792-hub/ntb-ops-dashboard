import json

tpath = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\4336314d-71dd-4e55-8828-c64201e3d4a3\.system_generated\logs\transcript.jsonl"
with open(tpath, 'r', encoding='utf-8') as f:
    steps = [json.loads(line) for line in f]

for i in range(15, min(100, len(steps))):
    step = steps[i]
    print(f"Step {step.get('step_index')}: source={step.get('source')} type={step.get('type')} status={step.get('status')}")
    if step.get('tool_calls'):
        for tc in step['tool_calls']:
            print(f"  Tool: {tc.get('name')}")
            if tc.get('name') == 'browser_subagent':
                print(f"    TaskName: {tc.get('args', {}).get('TaskName')}")
            if tc.get('name') == 'run_command':
                print(f"    Cmd: {tc.get('args', {}).get('CommandLine')}")

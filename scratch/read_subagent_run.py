import json

tpath = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\4336314d-71dd-4e55-8828-c64201e3d4a3\.system_generated\logs\transcript.jsonl"
print("Tool calls in CURRENT conversation:")
with open(tpath, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            step = data.get('step_index')
            tc_list = data.get('tool_calls', [])
            for tc in tc_list:
                name = tc.get('name')
                args = tc.get('args', {})
                if name in ['write_to_file', 'replace_file_content', 'multi_replace_file_content', 'run_command']:
                    print(f"  Step {step}: {name} with args keys: {list(args.keys())}")
                    if 'CommandLine' in args:
                        print(f"    Cmd: {args['CommandLine']}")
                    if 'Description' in args:
                        print(f"    Desc: {args['Description']}")
        except Exception as e:
            pass

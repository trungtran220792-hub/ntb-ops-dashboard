import json

log_path = r'C:\Users\lap4all\.gemini\antigravity-ide\brain\4336314d-71dd-4e55-8828-c64201e3d4a3\.system_generated\logs\transcript.jsonl'

keywords = ['table-nhan-su-body', 'renderNhanSuTable', 'loadNhanSuData', 'ns-total-hc', 'ns-input-global-growth', 'tab-nhan-su']

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            step = json.loads(line)
            if 'tool_calls' in step:
                for call in step['tool_calls']:
                    if call.get('name') in ['replace_file_content', 'multi_replace_file_content', 'write_to_file']:
                        args = call.get('args', {})
                        args_str = json.dumps(args, ensure_ascii=False)
                        if any(kw in args_str for kw in keywords):
                            step_idx = step.get('step_index')
                            print(f"=== FOUND TOOL CALL IN STEP {step_idx} ===")
                            print("Tool:", call.get('name'))
                            if 'TargetFile' in args:
                                print("TargetFile:", args['TargetFile'])
                            if 'Instruction' in args:
                                print("Instruction:", args['Instruction'])
                            
                            # Handle ReplacementContent
                            content = None
                            if 'ReplacementContent' in args:
                                content = args['ReplacementContent']
                            elif 'CodeContent' in args:
                                content = args['CodeContent']
                            
                            if content:
                                print(f"Content length: {len(content)}")
                                out_fn = f"scratch/extracted_step_{step_idx}.txt"
                                with open(out_fn, 'w', encoding='utf-8') as out_f:
                                    out_f.write(content)
                                print(f"Saved full content to {out_fn}")
        except Exception as e:
            print("Error parsing line:", e)

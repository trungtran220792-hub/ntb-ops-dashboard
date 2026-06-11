import json
import os

past_conv_id = "12824642-463c-46a9-9dc4-473af4f03ce9"
transcript_path = fr"C:\Users\lap4all\.gemini\antigravity-ide\brain\{past_conv_id}\.system_generated\logs\transcript.jsonl"
output_path = r"c:\Users\lap4all\Desktop\New folder\scratch\past_odr_diffs.txt"

if not os.path.exists(transcript_path):
    print(f"Path does not exist: {transcript_path}")
    exit(1)

with open(transcript_path, 'r', encoding='utf-8') as f:
    with open(output_path, 'w', encoding='utf-8') as out:
        for line in f:
            try:
                data = json.loads(line)
                if 'tool_calls' in data and data['tool_calls']:
                    tc = data['tool_calls'][0]
                    if tc.get('name') in ['replace_file_content', 'multi_replace_file_content']:
                        args = tc.get('args', {})
                        target_file = args.get('TargetFile', '')
                        if 'index.html' in target_file:
                            repl = str(args.get('ReplacementContent', ''))
                            if 'odr' in repl.lower():
                                out.write(f"=== STEP {data.get('step_index')} ===\n")
                                out.write(f"Tool: {tc.get('name')}\n")
                                out.write(f"TargetContent:\n{args.get('TargetContent')}\n")
                                out.write(f"ReplacementContent:\n{args.get('ReplacementContent')}\n\n")
            except Exception as e:
                pass
print("Wrote ODR results to scratch/past_odr_diffs.txt")

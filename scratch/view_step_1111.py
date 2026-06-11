import json
import os

past_conv_id = "12824642-463c-46a9-9dc4-473af4f03ce9"
transcript_path = fr"C:\Users\lap4all\.gemini\antigravity-ide\brain\{past_conv_id}\.system_generated\logs\transcript.jsonl"
output_path = r"c:\Users\lap4all\Desktop\New folder\scratch\step_1111_details.txt"

if not os.path.exists(transcript_path):
    print("Log not found")
    exit(1)

with open(transcript_path, 'r', encoding='utf-8') as f:
    with open(output_path, 'w', encoding='utf-8') as out:
        for line in f:
            try:
                data = json.loads(line)
                step_idx = data.get('step_index')
                if step_idx in [1104, 1110, 1111, 1112, 1154, 1155, 1156, 1238, 1250]:
                    out.write(f"=== STEP {step_idx} ===\n")
                    out.write(f"Type: {data.get('type')}, Source: {data.get('source')}\n")
                    if 'tool_calls' in data and data['tool_calls']:
                        tc = data['tool_calls'][0]
                        out.write(f"Tool: {tc.get('name')}\n")
                        args = tc.get('args', {})
                        out.write("Arguments:\n")
                        for k, v in args.items():
                            if k in ['TargetContent', 'ReplacementContent']:
                                # Limit printing length to avoid huge logs
                                val_str = str(v)
                                out.write(f"  {k} (length {len(val_str)}):\n")
                                out.write(val_str[:500] + "\n... [truncated in print] ...\n" if len(val_str) > 500 else val_str + "\n")
                            else:
                                out.write(f"  {k}: {repr(v)}\n")
                    out.write("\n")
            except Exception as e:
                pass
print("Wrote details to scratch/step_1111_details.txt")

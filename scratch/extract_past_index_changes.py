import json
import codecs

past_conv_id = "12824642-463c-46a9-9dc4-473af4f03ce9"
transcript_path = fr"C:\Users\lap4all\.gemini\antigravity-ide\brain\{past_conv_id}\.system_generated\logs\transcript.jsonl"
output_path = r"c:\Users\lap4all\Desktop\New folder\scratch\extracted_past_index_changes.txt"

def decode_log_string(s):
    if not isinstance(s, str):
        return s
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
    try:
        return codecs.escape_decode(bytes(s, 'utf-8'))[0].decode('utf-8').replace('\r\n', '\n')
    except Exception:
        return s

with open(transcript_path, 'r', encoding='utf-8') as f, open(output_path, 'w', encoding='utf-8') as out:
    for line in f:
        try:
            data = json.loads(line)
            step_idx = data.get('step_index')
            if 'tool_calls' in data and data['tool_calls']:
                for tc in data['tool_calls']:
                    if tc.get('name') in ['replace_file_content', 'multi_replace_file_content']:
                        args = tc.get('args', {})
                        target_file = args.get('TargetFile', '')
                        if 'index.html' in target_file:
                            out.write(f"=== STEP {step_idx} ===\n")
                            out.write(f"Description: {args.get('Description')}\n")
                            out.write(f"Instruction: {args.get('Instruction')}\n")
                            if 'ReplacementChunks' in args:
                                chunks = args['ReplacementChunks']
                                if isinstance(chunks, str):
                                    try:
                                        chunks = json.loads(chunks)
                                    except Exception:
                                        pass
                                out.write(f"ReplacementChunks: {json.dumps(chunks, indent=2, ensure_ascii=False)}\n\n")
                            else:
                                out.write(f"TargetContent:\n{args.get('TargetContent')}\n")
                                out.write(f"ReplacementContent:\n{args.get('ReplacementContent')}\n\n")
        except Exception as e:
            out.write(f"Error parsing line: {e}\n")

print("Done. Check scratch/extracted_past_index_changes.txt")

import json
import os

target_conv_id = "0d711590-0357-43ee-a937-04cabf62a0ba"
transcript_path = fr"C:\Users\lap4all\.gemini\antigravity-ide\brain\{target_conv_id}\.system_generated\logs\transcript.jsonl"
output_path = r"c:\Users\lap4all\Desktop\New folder\scratch\extracted_0d711590_index_changes.txt"

if not os.path.exists(transcript_path):
    print("Transcript not found at", transcript_path)
    exit(1)

with open(transcript_path, 'r', encoding='utf-8') as f, open(output_path, 'w', encoding='utf-8') as out:
    for line in f:
        try:
            data = json.loads(line)
            step_idx = data.get('step_index')
            if 'tool_calls' in data and data['tool_calls']:
                for tc in data['tool_calls']:
                    name = tc.get('name')
                    if name in ['replace_file_content', 'multi_replace_file_content', 'write_to_file']:
                        args = tc.get('args', {})
                        target_file = args.get('TargetFile', '')
                        if 'index.html' in target_file:
                            out.write(f"=== STEP {step_idx} - Tool Call: {name} ===\n")
                            out.write(f"Description: {args.get('Description')}\n")
                            out.write(f"Instruction: {args.get('Instruction')}\n")
                            if name == 'replace_file_content':
                                out.write("--- TARGET CONTENT ---\n")
                                out.write(f"{args.get('TargetContent')}\n")
                                out.write("--- REPLACEMENT CONTENT ---\n")
                                out.write(f"{args.get('ReplacementContent')}\n")
                            elif name == 'multi_replace_file_content':
                                out.write("--- CHUNKS ---\n")
                                chunks = args.get('ReplacementChunks', [])
                                out.write(json.dumps(chunks, indent=2, ensure_ascii=False) + "\n")
                            elif name == 'write_to_file':
                                out.write("--- WRITE TO FILE (Content length: {}) ---\n".format(len(args.get('CodeContent', ''))))
                                if len(args.get('CodeContent', '')) < 10000:
                                    out.write(args.get('CodeContent', '') + "\n")
                            out.write("\n" + "="*40 + "\n\n")
        except Exception as e:
            out.write(f"Error parsing line: {e}\n")

print("Done extracting changes for 0d711590.")

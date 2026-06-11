# -*- coding: utf-8 -*-
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

transcript_path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\92726133-7314-4954-9f94-c885d0c26df2\.system_generated\logs\transcript.jsonl"
out_dir = r"c:\Users\lap4all\Desktop\New folder\scratch\extracted_steps"
os.makedirs(out_dir, exist_ok=True)

target_steps = [133, 147, 351, 587, 593, 837, 843, 1011, 1127, 1131, 1157, 1167, 1171, 1177, 1405, 1407, 1411, 1415, 1419, 1441, 1445, 1449, 1453]

if os.path.exists(transcript_path):
    print("Found transcript file. Parsing lines...")
    with open(transcript_path, 'r', encoding='utf-8', errors='ignore') as f:
        for idx, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                step_index = data.get('step_index')
                if step_index in target_steps:
                    tool_calls = data.get('tool_calls', [])
                    for tc in tool_calls:
                        name = tc.get('name')
                        args = tc.get('args', {})
                        target_file = args.get('TargetFile', '')
                        if name in ['replace_file_content', 'multi_replace_file_content', 'write_to_file'] and 'index.html' in target_file:
                            instruction = args.get('Instruction', '')
                            out_filename = os.path.join(out_dir, f"step_{step_index}.txt")
                            with open(out_filename, 'w', encoding='utf-8') as out_f:
                                out_f.write(f"=== STEP {step_index} | Tool: {name} ===\n")
                                out_f.write(f"Description: {args.get('Description')}\n")
                                out_f.write(f"Instruction: {instruction}\n\n")
                                if name == 'replace_file_content':
                                    out_f.write("--- TARGET CONTENT ---\n")
                                    out_f.write(args.get('TargetContent', '') + "\n\n")
                                    out_f.write("--- REPLACEMENT CONTENT ---\n")
                                    out_f.write(args.get('ReplacementContent', '') + "\n")
                                elif name == 'multi_replace_file_content':
                                    chunks = args.get('ReplacementChunks', [])
                                    out_f.write("--- MULTI CHUNKS ---\n")
                                    for c_idx, chunk in enumerate(chunks):
                                        out_f.write(f"  Chunk {c_idx}:\n")
                                        out_f.write(f"    StartLine: {chunk.get('StartLine')}, EndLine: {chunk.get('EndLine')}\n")
                                        out_f.write("    TargetContent:\n")
                                        out_f.write(chunk.get('TargetContent', '') + "\n")
                                        out_f.write("    ReplacementContent:\n")
                                        out_f.write(chunk.get('ReplacementContent', '') + "\n")
                            print(f"Saved step {step_index} details to {out_filename}")
            except Exception as e:
                pass
else:
    print("Transcript not found.")

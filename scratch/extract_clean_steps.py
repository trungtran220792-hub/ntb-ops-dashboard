import json
import os

target_conv_id = "0d711590-0357-43ee-a937-04cabf62a0ba"
transcript_path = fr"C:\Users\lap4all\.gemini\antigravity-ide\brain\{target_conv_id}\.system_generated\logs\transcript.jsonl"
output_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"

if not os.path.exists(transcript_path):
    print("Transcript not found at", transcript_path)
    exit(1)

steps_to_extract = [64, 73, 151, 157, 544]

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            step_idx = data.get('step_index')
            if step_idx in steps_to_extract:
                print(f"Extracting step {step_idx}...")
                if 'tool_calls' in data and data['tool_calls']:
                    for idx, tc in enumerate(data['tool_calls']):
                        args = tc.get('args', {})
                        name = tc.get('name')
                        
                        # Save the target content
                        if 'TargetContent' in args:
                            target_file_path = os.path.join(output_dir, f"step_{step_idx}_target.txt")
                            with open(target_file_path, 'w', encoding='utf-8') as tf:
                                tf.write(args['TargetContent'])
                                
                        # Save the replacement content
                        if 'ReplacementContent' in args:
                            repl_file_path = os.path.join(output_dir, f"step_{step_idx}_repl.txt")
                            with open(repl_file_path, 'w', encoding='utf-8') as rf:
                                rf.write(args['ReplacementContent'])
                                
                        # For multi-replace
                        if 'ReplacementChunks' in args:
                            chunks_file_path = os.path.join(output_dir, f"step_{step_idx}_chunks.json")
                            with open(chunks_file_path, 'w', encoding='utf-8') as cf:
                                json.dump(args['ReplacementChunks'], cf, indent=2, ensure_ascii=False)
                                
        except Exception as e:
            print(f"Error parsing line for step {step_idx}: {e}")

print("Extraction completed successfully!")

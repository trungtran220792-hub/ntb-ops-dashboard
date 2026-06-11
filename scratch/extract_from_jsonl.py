# -*- coding: utf-8 -*-
import json
import os

transcript_paths = [
    r"C:\Users\lap4all\.gemini\antigravity-ide\brain\4336314d-71dd-4e55-8828-c64201e3d4a3\.system_generated\logs\transcript.jsonl",
    r"C:\Users\lap4all\.gemini\antigravity-ide\brain\92726133-7314-4954-9f94-c885d0c26df2\.system_generated\logs\transcript.jsonl"
]

out_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"

for path in transcript_paths:
    if not os.path.exists(path):
        print("Does not exist:", path)
        continue
    
    print("Parsing:", path)
    base_name = os.path.basename(os.path.dirname(os.path.dirname(path)))
    
    with open(path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f):
            try:
                data = json.loads(line)
                # We are looking for tool_calls that modify index.html
                # Check if it has 'tool_calls'
                tool_calls = data.get("tool_calls", [])
                for tc in tool_calls:
                    args = tc.get("args", {})
                    if not args:
                        continue
                    
                    # check if TargetFile matches index.html
                    target_file = args.get("TargetFile", "")
                    if "index.html" in target_file:
                        # Print step index and description
                        step_idx = data.get("step_index", line_num)
                        print(f"  Step {step_idx}: {tc.get('name')} in {base_name}")
                        
                        # Let's inspect content in replacement chunks or replacement content
                        replacement = args.get("ReplacementContent", "")
                        chunks = args.get("ReplacementChunks", [])
                        code_content = args.get("CodeContent", "")
                        
                        # Save them to file
                        if replacement:
                            out_path = os.path.join(out_dir, f"raw_jsonl_{base_name}_step_{step_idx}_replacement.txt")
                            with open(out_path, "w", encoding="utf-8") as out_f:
                                out_f.write(replacement)
                            print(f"    Saved replacement ({len(replacement)} chars) to {os.path.basename(out_path)}")
                            
                        if chunks:
                            for c_idx, chunk in enumerate(chunks):
                                rep_chunk = chunk.get("ReplacementContent", "")
                                if rep_chunk:
                                    out_path = os.path.join(out_dir, f"raw_jsonl_{base_name}_step_{step_idx}_chunk_{c_idx}.txt")
                                    with open(out_path, "w", encoding="utf-8") as out_f:
                                        out_f.write(rep_chunk)
                                    print(f"    Saved chunk {c_idx} ({len(rep_chunk)} chars) to {os.path.basename(out_path)}")
                                    
                        if code_content:
                            out_path = os.path.join(out_dir, f"raw_jsonl_{base_name}_step_{step_idx}_code.txt")
                            with open(out_path, "w", encoding="utf-8") as out_f:
                                out_f.write(code_content)
                            print(f"    Saved code_content ({len(code_content)} chars) to {os.path.basename(out_path)}")
            except Exception as e:
                # print("Error parsing line:", line_num, str(e))
                pass
print("Done extracting raw JSONL tool arguments!")

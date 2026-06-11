import os
import json

transcript_path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\0d711590-0357-43ee-a937-04cabf62a0ba\.system_generated\logs\transcript.jsonl"
out = open(r"c:\Users\lap4all\Desktop\New folder\scratch\found_0d711590_tabs.txt", "w", encoding="utf-8")

if os.path.exists(transcript_path):
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            try:
                data = json.loads(line)
            except Exception as e:
                continue
            
            step = data.get('step_index')
            tool_calls = data.get('tool_calls', [])
            for tc in tool_calls:
                method = tc.get('name')
                args = tc.get('args', {})
                target_file = args.get('TargetFile', '')
                if 'index.html' in target_file:
                    out.write(f"Step {step} | Tool: {method}\n")
                    out.write(f"  Description: {args.get('Description')}\n")
                    out.write(f"  Instruction: {args.get('Instruction')}\n")
                    
                    target = args.get('TargetContent', '')
                    replace = args.get('ReplacementContent', '')
                    
                    out.write(f"  Target length: {len(target)} chars\n")
                    out.write(f"  Replacement length: {len(replace)} chars\n")
                    
                    # Print first 100 characters of target and replacement to see if they are truncated
                    out.write(f"  Target start: {repr(target[:100])}\n")
                    out.write(f"  Replace start: {repr(replace[:100])}\n")
                    out.write("\n")
else:
    print("Transcript not found")

out.close()
print("Done")

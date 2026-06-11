import json

transcript_path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\2742477c-f9ad-4ec9-923d-4fdf4f5c14ba\.system_generated\logs\transcript.jsonl"
out_path = r"c:\Users\lap4all\Desktop\New folder\scratch\extracted_step_1200_details.txt"

print(f"Reading {transcript_path}...")
results = []

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            step = json.loads(line)
            idx = step.get("step_index")
            if 1190 <= idx <= 1220:
                results.append(step)
        except Exception as e:
            pass

print(f"Found {len(results)} steps. Saving details to {out_path}...")
with open(out_path, 'w', encoding='utf-8') as out_f:
    for step in results:
        out_f.write(f"=========================================\n")
        out_f.write(f"Step {step.get('step_index')} | Type: {step.get('type')} | Source: {step.get('source')}\n")
        if step.get("content"):
            out_f.write(f"Content:\n{step.get('content')}\n")
        
        tool_calls = step.get("tool_calls")
        if tool_calls:
            out_f.write("Tool Calls:\n")
            for tc in tool_calls:
                out_f.write(f"  Tool: {tc.get('name')}\n")
                out_f.write(f"  Arguments:\n{json.dumps(tc.get('arguments'), indent=2, ensure_ascii=False)}\n")
        
        # Check if there is output in system messages or whatever
        out_f.write("\n")

print("Done!")

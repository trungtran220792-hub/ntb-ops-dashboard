import json
import os

transcript_path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\4336314d-71dd-4e55-8828-c64201e3d4a3\.system_generated\logs\transcript.jsonl"
output_path = r"scratch/pre_checkout_steps.txt"

with open(transcript_path, 'r', encoding='utf-8') as f, open(output_path, 'w', encoding='utf-8') as out:
    for line in f:
        try:
            data = json.loads(line)
            step_idx = data.get('step_index')
            if 40 <= step_idx <= 60:
                out.write(f"--- STEP {step_idx} ({data.get('type')}) ---\n")
                if 'thinking' in data and data['thinking']:
                    out.write("Thinking: " + data['thinking'] + "\n")
                if 'tool_calls' in data:
                    out.write(json.dumps(data['tool_calls'], indent=2, ensure_ascii=False) + "\n")
                if 'content' in data:
                    out.write(data['content'] + "\n")
                out.write("="*60 + "\n\n")
        except Exception as e:
            out.write(f"Error parsing line {step_idx if 'step_idx' in locals() else 'unknown'}: {e}\n")

print("Done. Saved output to scratch/pre_checkout_steps.txt")

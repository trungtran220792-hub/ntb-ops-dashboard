import json
import os

past_conv_id = "12824642-463c-46a9-9dc4-473af4f03ce9"
transcript_path = fr"C:\Users\lap4all\.gemini\antigravity-ide\brain\{past_conv_id}\.system_generated\logs\transcript.jsonl"
output_path = r"c:\Users\lap4all\Desktop\New folder\scratch\step_940_full.txt"

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        if data.get('step_index') == 940:
            with open(output_path, 'w', encoding='utf-8') as out:
                out.write(json.dumps(data, indent=2, ensure_ascii=False))
            print("Wrote full step 940 to scratch/step_940_full.txt")
            break

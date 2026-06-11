import os
import json

brain_dir = r"C:\Users\lap4all\.gemini\antigravity-ide\brain"
output_path = r"scratch/user_messages_recent.txt"

recent_sessions = [
    "9372904b-335a-4bb3-83f3-9f8d90d80b91",
    "0d711590-0357-43ee-a937-04cabf62a0ba",
    "4336314d-71dd-4e55-8828-c64201e3d4a3"
]

with open(output_path, 'w', encoding='utf-8') as out:
    for sess in recent_sessions:
        tpath = os.path.join(brain_dir, sess, ".system_generated", "logs", "transcript.jsonl")
        if not os.path.exists(tpath):
            continue
        
        out.write(f"\n========================================\n")
        out.write(f"SESSION: {sess}\n")
        out.write(f"========================================\n")
        
        with open(tpath, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    step = data.get('step_index')
                    source = data.get('source')
                    dtype = data.get('type')
                    if source == 'USER_EXPLICIT' or dtype == 'USER_INPUT':
                        content = data.get('content', '')
                        out.write(f"Step {step}: {content}\n")
                        out.write("-" * 40 + "\n")
                except Exception:
                    pass

print("Saved recent user messages to scratch/user_messages_recent.txt")

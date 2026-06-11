import json
import re

path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\2742477c-f9ad-4ec9-923d-4fdf4f5c14ba\.system_generated\logs\transcript.jsonl"
output = []

with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            step = json.loads(line)
            source = step.get('source')
            dtype = step.get('type')
            if source == 'USER_EXPLICIT' or dtype == 'USER_INPUT':
                content = step.get('content', '')
                step_idx = step.get('step_index')
                
                # Try to extract the local time from the metadata
                local_time = "Unknown"
                time_match = re.search(r"The current local time is:\s*([^\n]+)", content)
                if time_match:
                    local_time = time_match.group(1).strip()
                
                # Extract clean request message
                clean_content = content
                user_req_match = re.search(r"<USER_REQUEST>(.*?)</USER_REQUEST>", content, re.DOTALL)
                if user_req_match:
                    clean_content = user_req_match.group(1).strip()
                
                output.append(f"Step {step_idx} | Local Time: {local_time} | Request: {clean_content}")
        except Exception as e:
            pass

with open("scratch/all_user_requests.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print(f"Saved {len(output)} requests to scratch/all_user_requests.txt")

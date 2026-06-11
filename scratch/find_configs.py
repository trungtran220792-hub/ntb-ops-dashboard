import json
import re

log_file = r'C:\Users\lap4all\.gemini\antigravity-ide\brain\2742477c-f9ad-4ec9-923d-4fdf4f5c14ba\.system_generated\logs\transcript.jsonl'
configs_found = set()

# Pattern to search for key-value assignments or dictionary keys
pattern = re.compile(r'(TELEGRAM_BOT_TOKEN|TELEGRAM_CHAT_ID|GEMINI_API_KEY)["\'\s]*[:=]["\'\s]*([^"\'\\n,}]+)', re.IGNORECASE)

with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        for match in pattern.finditer(line):
            key, val = match.groups()
            configs_found.add((key.upper().strip(), val.strip()))

for key, val in sorted(configs_found):
    print(f"{key}: {val}")

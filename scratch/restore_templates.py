import json
import os
import codecs
import sys

sys.stdout.reconfigure(encoding='utf-8')

transcript_path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\92726133-7314-4954-9f94-c885d0c26df2\.system_generated\logs\transcript.jsonl"
index_html_path = r"c:\Users\lap4all\Desktop\New folder\templates\index.html"

# Load the transcript steps
step_133_args = None
step_147_args = None

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        if data.get('step_index') == 133:
            step_133_args = data['tool_calls'][0]['args']
        elif data.get('step_index') == 147:
            step_147_args = data['tool_calls'][0]['args']

if not step_133_args or not step_147_args:
    print("Error: Could not find step 133 or 147 in the logs.")
    exit(1)

# Read index.html
with open(index_html_path, 'r', encoding='utf-8') as f:
    content = f.read().replace('\r\n', '\n')

def decode_log_string(s):
    if not isinstance(s, str):
        return s
    # Strip wrapping double quotes from serialized string
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
    # Decode backslash escapes safely
    return codecs.escape_decode(bytes(s, 'utf-8'))[0].decode('utf-8').replace('\r\n', '\n')

# Parse TargetContent and ReplacementContent
target_133 = decode_log_string(step_133_args['TargetContent'])
replace_133 = decode_log_string(step_133_args['ReplacementContent'])

print("Target 133 length:", len(target_133))
print("Replace 133 length:", len(replace_133))

target_133_stripped = target_133.strip()
idx_133 = content.find(target_133_stripped)

if idx_133 != -1:
    # We replace the matched stripped block, maintaining any leading indent if necessary
    # Or just slice-replace:
    content = content[:idx_133] + replace_133 + content[idx_133 + len(target_133_stripped):]
    print("Successfully applied Step 133 HTML redesign.")
else:
    print("Error: Step 133 TargetContent (stripped) not found in index.html.")
    exit(1)

target_147 = decode_log_string(step_147_args['TargetContent'])
replace_147 = decode_log_string(step_147_args['ReplacementContent'])

print("Target 147 length:", len(target_147))
print("Replace 147 length:", len(replace_147))

if target_147 in content:
    content = content.replace(target_147, replace_147)
    print("Successfully applied Step 147 JS logic redesign.")
else:
    print("Error: Step 147 TargetContent not found in index.html.")
    print("Target starts with:", repr(target_147[:200]))
    exit(1)

# Write index.html back
with open(index_html_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("index.html fully restored to redesigned state.")

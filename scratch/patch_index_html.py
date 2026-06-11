import os
import json
import codecs
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

brain_dir = r"C:\Users\lap4all\.gemini\antigravity-ide\brain"
conv_ids = [
    '92726133-7314-4954-9f94-c885d0c26df2',
    '8c4a74de-9016-4159-9f42-08c9862c9b0d',
    '12824642-463c-46a9-9dc4-473af4f03ce9',
    '9372904b-335a-4bb3-83f3-9f8d90d80b91',
    '0d711590-0357-43ee-a937-04cabf62a0ba'
]

def clean_log_value(val):
    if val is None:
        return ""
    if not isinstance(val, str):
        return str(val)
    # Strip wrapping double quotes from serialized string
    if val.startswith('"') and val.endswith('"') and len(val) >= 2:
        val = val[1:-1]
    # Decode backslash escapes safely
    try:
        return codecs.escape_decode(bytes(val, 'utf-8'))[0].decode('utf-8').replace('\r\n', '\n')
    except Exception:
        return val.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace("\\'", "'").replace('\\\\', '\\')

all_edits = []

for c_idx, cid in enumerate(conv_ids):
    tpath = os.path.join(brain_dir, cid, ".system_generated", "logs", "transcript.jsonl")
    if not os.path.exists(tpath):
        continue
    
    with open(tpath, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                step = data.get('step_index')
                tc_list = data.get('tool_calls', [])
                for tc in tc_list:
                    name = tc.get('name')
                    args = tc.get('args', {})
                    if name in ['replace_file_content', 'multi_replace_file_content']:
                        tgt = args.get('TargetFile', '')
                        if 'index.html' in tgt or 'app.py' in tgt:
                            file_type = 'index.html' if 'index.html' in tgt else 'app.py'
                            all_edits.append({
                                'conv_idx': c_idx,
                                'conv_id': cid,
                                'step': step,
                                'tool': name,
                                'file_type': file_type,
                                'args': args
                            })
            except Exception as e:
                pass

# Sort edits by conv_idx and step_index
all_edits.sort(key=lambda x: (x['conv_idx'], x['step']))

# Fetch base files from git directly
app_content = subprocess.check_output(['git', 'show', '3cdad023:app.py']).decode('utf-8').replace('\r\n', '\n')
index_content = subprocess.check_output(['git', 'show', '3cdad023:templates/index.html']).decode('utf-8').replace('\r\n', '\n')

print(f"Loaded base files directly from Git. App len: {len(app_content)}, Index len: {len(index_content)}")

applied_count = 0
failed_count = 0

for edit in all_edits:
    cid = edit['conv_id'][:8]
    step = edit['step']
    tool = edit['tool']
    ftype = edit['file_type']
    args = edit['args']
    desc = args.get('Description', 'no desc')
    
    current_content = app_content if ftype == 'app.py' else index_content
    
    if tool == 'replace_file_content':
        target = clean_log_value(args.get('TargetContent'))
        replacement = clean_log_value(args.get('ReplacementContent'))
        
        # Check if target is truncated
        is_truncated = False
        if (target and '<truncated' in target) or (replacement and '<truncated' in replacement):
            is_truncated = True
            
        if is_truncated:
            print(f"[{cid} S{step}] Skip truncated edit for {ftype}. Desc: {desc[:50]}")
            failed_count += 1
            continue
            
        if not target:
            print(f"[{cid} S{step}] Skip empty TargetContent for {ftype}")
            continue
            
        if target in current_content:
            current_content = current_content.replace(target, replacement)
            applied_count += 1
        else:
            target_stripped = target.strip()
            if target_stripped and target_stripped in current_content:
                idx = current_content.find(target_stripped)
                current_content = current_content[:idx] + replacement + current_content[idx + len(target_stripped):]
                applied_count += 1
            else:
                print(f"[{cid} S{step}] Failed replace_file_content to {ftype}. Desc: {desc[:50]}")
                failed_count += 1
                
    elif tool == 'multi_replace_file_content':
        chunks = args.get('ReplacementChunks', [])
        if isinstance(chunks, str):
            try:
                chunks = json.loads(chunks)
            except Exception:
                pass
        
        if not isinstance(chunks, list):
            print(f"[{cid} S{step}] Multi replace chunks is not list")
            failed_count += 1
            continue
            
        is_truncated = False
        for chunk in chunks:
            target = clean_log_value(chunk.get('TargetContent'))
            replacement = clean_log_value(chunk.get('ReplacementContent'))
            if (target and '<truncated' in target) or (replacement and '<truncated' in replacement):
                is_truncated = True
                break
                
        if is_truncated:
            print(f"[{cid} S{step}] Skip truncated multi edit for {ftype}. Desc: {desc[:50]}")
            failed_count += 1
            continue
            
        success = True
        temp_content = current_content
        for chunk_idx, chunk in enumerate(chunks):
            target = clean_log_value(chunk.get('TargetContent'))
            replacement = clean_log_value(chunk.get('ReplacementContent'))
            
            if not target:
                continue
                
            if target in temp_content:
                temp_content = temp_content.replace(target, replacement)
            else:
                target_stripped = target.strip()
                if target_stripped and target_stripped in temp_content:
                    idx = temp_content.find(target_stripped)
                    temp_content = temp_content[:idx] + replacement + temp_content[idx + len(target_stripped):]
                else:
                    success = False
                    
        if success:
            current_content = temp_content
            applied_count += 1
        else:
            print(f"[{cid} S{step}] Failed multi_replace_file_content to {ftype}. Desc: {desc[:50]}")
            failed_count += 1
            
    if ftype == 'app.py':
        app_content = current_content
    else:
        index_content = current_content

print(f"Done patching. Applied: {applied_count}, Failed: {failed_count}")
print(f"Patched App len: {len(app_content)}, Patched Index len: {len(index_content)}")

with open(r"scratch\app.py.patched", "w", encoding="utf-8") as f:
    f.write(app_content)

with open(r"scratch\index.html.patched", "w", encoding="utf-8") as f:
    f.write(index_content)

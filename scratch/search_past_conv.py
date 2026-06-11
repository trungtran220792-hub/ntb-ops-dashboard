import os
import json
import re

brain_dir = r"C:\Users\lap4all\.gemini\antigravity-ide\brain"
output_path = r"scratch/past_conversations_search.txt"

keywords = [
    re.compile(r"chỉ số NTB", re.IGNORECASE),
    re.compile(r"opr tts", re.IGNORECASE),
    re.compile(r"giới thiệu lên đầu", re.IGNORECASE),
    re.compile(r"phiên bản ngon lành", re.IGNORECASE),
    re.compile(r"phục hồi", re.IGNORECASE),
    re.compile(r"chất lượng", re.IGNORECASE)
]

results = []

for cid in os.listdir(brain_dir):
    tpath = os.path.join(brain_dir, cid, ".system_generated", "logs", "transcript.jsonl")
    if not os.path.exists(tpath):
        continue
    
    with open(tpath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                step = data.get('step_index')
                content = data.get('content', '')
                if not content:
                    continue
                
                # Check keywords
                matched = []
                for kw in keywords:
                    if kw.search(content):
                        matched.append(kw.pattern)
                
                if matched:
                    results.append({
                        'cid': cid,
                        'step': step,
                        'matched': matched,
                        'content': content[:1000] # print first 1000 chars of content
                    })
            except Exception:
                pass

# Sort results by conversation folder name/mtime
results.sort(key=lambda x: x['cid'])

with open(output_path, 'w', encoding='utf-8') as out:
    for res in results:
        out.write(f"========================================\n")
        out.write(f"CONV: {res['cid']} - STEP {res['step']}\n")
        out.write(f"Matched keywords: {', '.join(res['matched'])}\n")
        out.write(f"Content snippet:\n{res['content']}\n")
        out.write(f"========================================\n\n")

print(f"Done searching. Found {len(results)} matches. Check scratch/past_conversations_search.txt")

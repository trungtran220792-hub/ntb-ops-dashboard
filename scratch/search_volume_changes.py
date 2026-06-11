import json
import re

transcript_path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\2742477c-f9ad-4ec9-923d-4fdf4f5c14ba\.system_generated\logs\transcript.jsonl"
out_path = r"c:\Users\lap4all\Desktop\New folder\scratch\volume_search_results.txt"

print(f"Reading {transcript_path}...")
results = []

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            step = json.loads(line)
            content = step.get("content", "") or ""
            tool_calls = step.get("tool_calls", []) or []
            
            # Check content
            if "volume-creation" in content or "volume" in content or "tạo đơn" in content:
                results.append({
                    "step_index": step.get("step_index"),
                    "type": step.get("type"),
                    "source": step.get("source"),
                    "snippet": content[:300]
                })
            
            # Check tool calls
            for tc in tool_calls:
                args_str = json.dumps(tc.get("arguments", {}))
                if "volume-creation" in args_str or "volume" in args_str or "tạo đơn" in args_str:
                    results.append({
                        "step_index": step.get("step_index"),
                        "type": step.get("type") + "_tool_call",
                        "source": step.get("source"),
                        "snippet": args_str[:300]
                    })
        except Exception as e:
            pass

print(f"Found {len(results)} matches. Saving to {out_path}...")
with open(out_path, 'w', encoding='utf-8') as out_f:
    for r in results:
        out_f.write(f"=== Step {r['step_index']} ({r['type']}) from {r['source']} ===\n")
        out_f.write(r['snippet'] + "\n\n")

print("Done!")

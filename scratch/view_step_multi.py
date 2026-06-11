# -*- coding: utf-8 -*-
import os
import json

transcript_path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\2742477c-f9ad-4ec9-923d-4fdf4f5c14ba\.system_generated\logs\transcript.jsonl"
out_path = r"c:\Users\lap4all\Desktop\New folder\scratch\step_details_extracted.txt"

results = []
if os.path.exists(transcript_path):
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                step = json.loads(line)
            except:
                continue
            
            step_idx = step.get("step_index")
            # Check if this step has any tool calls
            tcs = step.get("tool_calls", [])
            for tc in tcs:
                args = tc.get("args", {})
                args_str = json.dumps(args, ensure_ascii=False).lower()
                keywords = ["nhân sự", "nhan_su", "nhan-su", "quản lý nhân sự"]
                if any(kw in args_str for kw in keywords):
                    results.append(f"=========================================================")
                    results.append(f"STEP: {step_idx} | Tool: {tc.get('name')} | Type: {step.get('type')}")
                    results.append(f"=========================================================")
                    
                    # Print target file and arguments
                    target_file = args.get("TargetFile") or args.get("Target")
                    if target_file:
                        results.append(f"TargetFile: {target_file}")
                    
                    for k, v in args.items():
                        if k not in ["TargetFile", "Target"]:
                            val_str = str(v)
                            # Let's print full value if it's less than 4000 characters
                            if len(val_str) > 4000:
                                results.append(f"  {k} (truncated length={len(val_str)}):")
                                results.append(val_str[:1500] + "\n... [TRUNCATED] ...\n" + val_str[-1500:])
                            else:
                                results.append(f"  {k}: {val_str}")
                    results.append("\n")

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(results))
    print(f"Saved step details to {out_path}")
else:
    print(f"Transcript not found at {transcript_path}")

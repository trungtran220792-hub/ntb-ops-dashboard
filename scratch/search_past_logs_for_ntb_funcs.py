import json
import os

brain_dir = r"C:\Users\lap4all\.gemini\antigravity-ide\brain"
output_path = r"scratch/past_ntb_funcs_found.txt"

funcs = ["cachedNtbMatrixData", "switchNtbRegion", "renderNtbKpiCards", "opr-overall-rate", "renderOprDashboard", "sort-am-asc", "renderNtbSummaryData"]

results = []

for cid in os.listdir(brain_dir):
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
                    content_str = json.dumps(args, ensure_ascii=False)
                    found = [func for func in funcs if func in content_str]
                    if found:
                        results.append({
                            'cid': cid,
                            'step': step,
                            'tool': name,
                            'found': found,
                            'args': args
                        })
            except Exception:
                pass

with open(output_path, 'w', encoding='utf-8') as out:
    for res in results:
        out.write(f"========================================\n")
        out.write(f"CONV: {res['cid']} - STEP {res['step']} - TOOL: {res['tool']}\n")
        out.write(f"Matched: {res['found']}\n")
        out.write(f"Description: {res['args'].get('Description')}\n")
        out.write(f"Instruction: {res['args'].get('Instruction')}\n")
        if res['tool'] == 'replace_file_content':
            out.write("--- TARGET CONTENT ---\n")
            out.write(f"{res['args'].get('TargetContent')}\n")
            out.write("--- REPLACEMENT CONTENT ---\n")
            out.write(f"{res['args'].get('ReplacementContent')}\n")
        elif res['tool'] == 'multi_replace_file_content':
            out.write("--- CHUNKS ---\n")
            out.write(json.dumps(res['args'].get('ReplacementChunks', []), indent=2, ensure_ascii=False) + "\n")
        out.write("========================================\n\n")

print(f"Done. Found {len(results)} occurrences. Results saved to scratch/past_ntb_funcs_found.txt")

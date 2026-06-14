import json

transcript_path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\99fae90b-413f-4302-ba67-0dea689b73b1\.system_generated\logs\transcript.jsonl"

try:
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            obj = json.loads(line)
            if "capture_browser_console_logs" in str(obj):
                print(f"Step {obj.get('step_index')}: {obj.get('type')} / {obj.get('status')}")
                # Print keys
                # print("Keys:", obj.keys())
                if "content" in obj:
                    print("Content:", obj["content"][:1000])
                print("="*80)
except Exception as e:
    print("Error:", str(e))

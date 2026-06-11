import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
scratch_dir = 'scratch'
for fn in os.listdir(scratch_dir):
    if fn.endswith('.py') or fn.endswith('.txt') or fn.endswith('.jsonl') or fn.endswith('.json'):
        path = os.path.join(scratch_dir, fn)
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                matches = re.findall(r'https://docs\.google\.com/spreadsheets/d/[a-zA-Z0-9-_/]+(?:edit|export)?(?:\?gid=\d+)?', content)
                if matches:
                    print(f'=== {fn} ===')
                    for m in set(matches):
                        print('  ', m)
        except Exception as e:
            pass

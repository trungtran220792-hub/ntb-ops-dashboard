import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('templates/index.html', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if 'comparison' in line or 'gtc-comparison' in line or 'gan-comparison' in line:
            if idx > 4000: # only look at script section
                print(f"Line {idx+1}: {line.strip()}")

in_script = False
with open('templates/index.html', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        if '<script' in line:
            in_script = True
        if '</script>' in line:
            in_script = False
        if in_script and 'ntb-trend' in line:
            print(f"Line {idx}: {line.strip()}")

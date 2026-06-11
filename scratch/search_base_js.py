with open('scratch/index.html.base', 'r', encoding='utf-16') as f:
    for idx, line in enumerate(f, 1):
        if 'ntb-trend-ltc' in line or 'ntb-trend-gtc' in line:
            # check if it is part of javascript (not raw HTML definition)
            if '=' in line or 'document.get' in line or 'querySelector' in line:
                print(f"Line {idx}: {line.strip()}")

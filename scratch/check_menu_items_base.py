with open('scratch/index.html.base', 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f, 1):
        if 'menu-item' in line or 'data-tab=' in line or 'content-panel' in line:
            if 'li ' in line or 'div ' in line or 'button ' in line:
                print(f"{idx}: {line.strip()}")

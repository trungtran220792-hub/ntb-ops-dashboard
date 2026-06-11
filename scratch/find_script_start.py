with open(r'c:\Users\lap4all\Desktop\New folder\templates\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
target_line = 4789
script_tag_line = -1

for idx in range(target_line - 1, -1, -1):
    if '<script' in lines[idx]:
        script_tag_line = idx + 1
        break

print(f"The opening <script> tag is on line: {script_tag_line}")
if script_tag_line != -1:
    print("Lines around start:")
    for i in range(max(0, script_tag_line - 5), min(len(lines), script_tag_line + 10)):
        print(f"L{i+1}: {lines[i]}")

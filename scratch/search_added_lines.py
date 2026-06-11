with open(r"c:\Users\lap4all\Desktop\New folder\scratch\added_lines.txt", 'r', encoding='utf-8') as f:
    lines = f.readlines()

found = False
for idx, line in enumerate(lines):
    if "opr-overall-rate" in line or "Báo Cáo Hiệu Suất OPR TTS" in line or "setAmOprSort" in line:
        found = True
        print(f"Line {idx+1}: {line.strip()}")
        # print context around the match
        start = max(0, idx - 10)
        end = min(len(lines), idx + 20)
        print("--- CONTEXT ---")
        for i in range(start, end):
            prefix = "+" if i == idx else " "
            print(f"{prefix}L{i+1}: {lines[i].strip()}")
        print("-" * 40)

if not found:
    print("No matches in added_lines.txt")

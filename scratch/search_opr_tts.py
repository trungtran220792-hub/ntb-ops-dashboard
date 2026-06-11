with open('templates/index.html', 'r', encoding='utf-8') as f_in:
    with open('scratch/opr_tts_logic.txt', 'w', encoding='utf-8') as f_out:
        for line_num, line in enumerate(f_in, 1):
            if 'opr' in line.lower() or 'gán' in line.lower() or 'gan' in line.lower():
                f_out.write(f"Line {line_num}: {line.strip()}\n")
print("Wrote output to scratch/opr_tts_logic.txt")

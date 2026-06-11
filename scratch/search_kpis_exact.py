with open('templates/index.html', 'r', encoding='utf-8') as f_in:
    with open('scratch/search_kpis_exact_output.txt', 'w', encoding='utf-8') as f_out:
        for line_num, line in enumerate(f_in, 1):
            line_lower = line.lower()
            if 'tts' in line_lower or 'gán' in line_lower:
                f_out.write(f"Line {line_num}: {line.strip()}\n")
print("Wrote output to scratch/search_kpis_exact_output.txt")

def run():
    with open("c:/Users/lap4all/Desktop/New folder/scratch/app_py_diff.txt", "r", encoding="utf-8") as f:
        diff_lines = f.readlines()

    sections = []
    current_section = []
    for line in diff_lines:
        if line.startswith("@@"):
            if current_section:
                sections.append(current_section)
            current_section = [line]
        elif current_section:
            current_section.append(line)
    if current_section:
        sections.append(current_section)

    out = []
    out.append(f"Total app.py diff sections: {len(sections)}")
    for i, sec in enumerate(sections):
        header = sec[0].strip()
        added = [l.strip() for l in sec if l.startswith("+") and not l.startswith("+++")]
        deleted = [l.strip() for l in sec if l.startswith("-") and not l.startswith("---")]
        out.append(f"\nSection {i+1}: {header}")
        out.append(f"  Deleted count: {len(deleted)}, Added count: {len(added)}")
        if deleted:
            out.append(f"  First deleted: {deleted[0][:150]}")
        if added:
            out.append(f"  First added:   {added[0][:150]}")

    with open("c:/Users/lap4all/Desktop/New folder/scratch/app_diff_summary.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))

run()
print("Saved app diff summary to scratch/app_diff_summary.txt")

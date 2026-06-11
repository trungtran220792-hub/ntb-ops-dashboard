import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

scratch_dir = "scratch"
files = [f for f in os.listdir(scratch_dir) if f.endswith(".txt") or f.endswith(".py")]

for f in files:
    fpath = os.path.join(scratch_dir, f)
    size = os.path.getsize(fpath)
    # Read first line
    try:
        with open(fpath, 'r', encoding='utf-8') as file:
            first_line = file.readline().strip()
    except Exception:
        try:
            with open(fpath, 'r', encoding='utf-16le') as file:
                first_line = file.readline().strip()
        except Exception:
            first_line = "<error reading>"
    # Strip BOM
    if first_line.startswith('\ufeff'):
        first_line = first_line[1:]
    print(f"{f} ({size} bytes): {first_line[:80]}")

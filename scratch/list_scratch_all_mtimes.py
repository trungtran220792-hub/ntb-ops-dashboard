import os
import datetime

scratch_dir = "scratch"
files = []
for f in os.listdir(scratch_dir):
    full_path = os.path.join(scratch_dir, f)
    if os.path.isfile(full_path):
        mtime = os.path.getmtime(full_path)
        size = os.path.getsize(full_path)
        files.append((f, size, mtime))

files.sort(key=lambda x: x[2], reverse=True)

with open("scratch/list_scratch_all_mtimes_res.txt", "w", encoding="utf-8") as out:
    for f in files:
        mtime_str = datetime.datetime.fromtimestamp(f[2]).strftime('%Y-%m-%d %H:%M:%S')
        out.write(f"{f[0]:<50} | {f[1]:>10} bytes | {mtime_str}\n")

print("Done listing.")

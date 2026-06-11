import os

paths_to_check = [
    '/tmp',
    'C:\\tmp',
    '\\tmp'
]

output = []
for p in paths_to_check:
    exists = os.path.exists(p)
    output.append(f"Path '{p}': exists={exists}")
    if exists:
        try:
            files = os.listdir(p)
            output.append(f"  Files: {files}")
            for f in files:
                f_path = os.path.join(p, f)
                stat = os.stat(f_path)
                output.append(f"    {f}: size={stat.st_size} bytes, mtime={stat.st_mtime}")
        except Exception as e:
            output.append(f"  Error listing: {e}")

# Check current working directory write access
output.append(f"\nCwd: {os.getcwd()}")
output.append(f"Cwd writeable: {os.access(os.getcwd(), os.W_OK)}")

with open('scratch/tmp_files_inspect.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
print("Done!")

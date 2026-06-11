import os

scratch_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"

decompressed_files = [f for f in os.listdir(scratch_dir) if "decompressed" in f]
print("Found decompressed files:", decompressed_files)

for df in decompressed_files:
    file_path = os.path.join(scratch_dir, df)
    print(f"File {df}: size = {os.path.getsize(file_path)} bytes")
    # check if they have opr-overall-rate
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    print(f"  Contains 'opr-overall-rate': {'opr-overall-rate' in content}")
    print(f"  Contains 'setAmOprSort': {'setAmOprSort' in content}")
    print(f"  Contains 'renderOprAmChartOnly': {'renderOprAmChartOnly' in content}")

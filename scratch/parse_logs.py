import os

log_path = 'server_output_new.log'
out_path = 'scratch/errors.txt'

if not os.path.exists('scratch'):
    os.makedirs('scratch')

try:
    with open(log_path, 'r', encoding='utf-16le') as f:
        lines = f.readlines()
    
    matching = []
    for line in lines:
        ll = line.lower()
        if any(x in ll for x in ['error', 'exception', 'loi', 'fail', 'sync']):
            matching.append(line.strip())
            
    with open(out_path, 'w', encoding='utf-8') as out:
        out.write(f"Total lines: {len(lines)}\n")
        out.write("Last 100 matching lines:\n")
        out.write('\n'.join(matching[-100:]))
    print("Success")
except Exception as e:
    print(f"Error: {e}")

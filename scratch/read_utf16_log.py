import sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = 'server_output_new.log'
try:
    with open(filepath, 'r', encoding='utf-16') as f:
        content = f.read()
    print("=== LOG CONTENT ===")
    print(content[-2000:])  # Print last 2000 characters
except Exception as e:
    print("Error reading log:", e)

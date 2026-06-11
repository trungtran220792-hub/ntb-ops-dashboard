import json
import os

output_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"

steps = [64, 73, 151, 157, 544]

for step in steps:
    for suffix in ['target', 'repl']:
        file_path = os.path.join(output_dir, f"step_{step}_{suffix}.txt")
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                
                # Check if it starts and ends with double quotes
                # Sometimes python json dump wraps the string value
                if content.startswith('"') and content.endswith('"'):
                    # Load as JSON string
                    decoded = json.loads(content)
                else:
                    # Try raw string escape decoding or json load anyway
                    # adding quotes to make it a valid json string
                    try:
                        decoded = json.loads('"' + content + '"')
                    except Exception as e:
                        decoded = content.encode('utf-8').decode('unicode_escape')
                
                clean_file_path = os.path.join(output_dir, f"step_{step}_{suffix}_clean.txt")
                with open(clean_file_path, 'w', encoding='utf-8') as f_out:
                    f_out.write(decoded)
                print(f"Decoded {file_path} -> {clean_file_path}")
            except Exception as e:
                print(f"Error decoding {file_path}: {e}")

print("Clean decoding completed!")

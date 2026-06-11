import os

src_path = r"c:\Users\lap4all\Desktop\New folder\scratch\step_1199_clean.txt"
dest_path = r"c:\Users\lap4all\Desktop\New folder\scratch\step_1199_formatted.txt"

if os.path.exists(src_path):
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Raw content length:", len(content))
    print("Starts with quote:", content.startswith('"'))
    print("Ends with quote:", content.endswith('"'))
    
    # If the file contains a JSON string representation, parse it
    try:
        if content.startswith('"'):
            # It's a JSON string literal. Let's load it.
            decoded = content
            # Try to parse it if it is JSON
            try:
                decoded = json.loads(content)
            except NameError:
                import json
                decoded = json.loads(content)
            content = decoded
    except Exception as e:
        print("Failed to decode JSON:", e)
    
    # Write to destination
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Wrote formatted content to:", dest_path)
    print("Formatted length:", len(content))
    print("Ends with:")
    print(content[-200:])
else:
    print("Source path does not exist.")

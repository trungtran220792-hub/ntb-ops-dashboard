import re

with open(r'c:\Users\lap4all\Desktop\New folder\scratch\console_from_details_res.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for "capture_browser_console_logs" block
# We can find matches and print what comes after
pattern = re.compile(r'capture_browser_console_logs.*?(?=\#\#\# Step|\Z)', re.DOTALL)
matches = pattern.findall(content)

with open(r'c:\Users\lap4all\Desktop\New folder\scratch\found_console_logs.txt', 'w', encoding='utf-8') as f_out:
    for i, match in enumerate(matches):
        f_out.write(f"Match {i+1}:\n{match}\n")
        f_out.write("="*40 + "\n")

print(f"Done. Found {len(matches)} occurrences of capture_browser_console_logs.")

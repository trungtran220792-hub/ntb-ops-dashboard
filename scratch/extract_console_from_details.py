import json

with open(r'c:\Users\lap4all\Desktop\New folder\scratch\subagent_details.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

content = data.get('content', '')

with open(r'c:\Users\lap4all\Desktop\New folder\scratch\console_from_details_res.txt', 'w', encoding='utf-8') as f_out:
    f_out.write("Content length: " + str(len(content)) + "\n")
    f_out.write(content)

print("Done. Saved to scratch/console_from_details_res.txt")

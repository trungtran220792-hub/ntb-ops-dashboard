import os

search_results_path = r"scratch/past_conversations_search.txt"
output_path = r"scratch/past_conversations_search_recent.txt"

recent_sessions = [
    "9372904b-335a-4bb3-83f3-9f8d90d80b91",
    "0d711590-0357-43ee-a937-04cabf62a0ba",
    "4336314d-71dd-4e55-8828-c64201e3d4a3"
]

with open(search_results_path, 'r', encoding='utf-8') as f, open(output_path, 'w', encoding='utf-8') as out:
    content = f.read()
    blocks = content.split("========================================\n\n")
    for block in blocks:
        is_recent = False
        for sess in recent_sessions:
            if sess in block:
                is_recent = True
                break
        if is_recent:
            out.write(block)
            out.write("========================================\n\n")

print("Filtered results saved to scratch/past_conversations_search_recent.txt")

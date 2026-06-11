import os

input_file = r"c:\Users\lap4all\Desktop\New folder\scratch\extracted_full_index_changes.txt"
output_dir = r"c:\Users\lap4all\Desktop\New folder\scratch\extracted_steps"
os.makedirs(output_dir, exist_ok=True)

current_conv = ""
current_step = ""
current_lines = []
is_capturing = False

steps_to_extract = {
    "0d711590-0357-43ee-a937-04cabf62a0ba": ["64", "73", "151", "157", "544"],
    "92726133-7314-4954-9f94-c885d0c26df2": [
        "133", "147", "351", "587", "593", "837", "843", "899", "1011",
        "1107", "1111", "1115", "1119", "1123", "1127", "1131", "1155",
        "1157", "1167", "1171", "1177", "1405", "1407", "1411", "1415",
        "1419", "1441", "1445", "1449", "1453"
    ]
}

def save_step(conv, step, lines):
    filename = f"{conv}_{step}.txt"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"Saved {filepath}")

with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith("=== CONVERSATION:"):
            current_conv = line.split(":")[-1].strip().split(" ")[0]
            continue
        
        if line.startswith("--- STEP"):
            # Save previous step if any
            if is_capturing and current_step:
                save_step(current_conv, current_step, current_lines)
            
            # Start new step
            step_part = line.split(" ")[2]
            current_step = step_part
            current_lines = [line]
            
            allowed_steps = steps_to_extract.get(current_conv, [])
            if current_step in allowed_steps:
                is_capturing = True
            else:
                is_capturing = False
            continue
        
        if is_capturing:
            current_lines.append(line)

# Save the last one
if is_capturing and current_step:
    save_step(current_conv, current_step, current_lines)

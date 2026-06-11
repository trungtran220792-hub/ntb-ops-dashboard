with open("c:/Users/lap4all/Desktop/New folder/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "/api/nhan-su" in line:
        print(f"Route defined at line {i+1}")
        print(f"Decorator is at line {i+2}: {lines[i+1].strip()}")
        break

with open(r"c:\Users\lap4all\Desktop\New folder\templates\index.html", 'r', encoding='utf-8') as f:
    content = f.read()

print("File size of templates/index.html:", len(content))

terms = ["getDeltaClass", "formatDelta", "delta_n1", "delta_wk"]
for term in terms:
    if term in content:
        # print line number and line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if term in line:
                print(f"Found '{term}' on line {i+1}: {line.strip()[:120]}")
    else:
        print(f"Term '{term}' NOT found in templates/index.html")

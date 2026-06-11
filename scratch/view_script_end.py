with open("c:/Users/lap4all/Desktop/New folder/templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()

with open("c:/Users/lap4all/Desktop/New folder/scratch/script_end.txt", "w", encoding="utf-8") as f:
    f.write(content[-3000:])

print("Saved last 3000 chars of templates/index.html to scratch/script_end.txt")

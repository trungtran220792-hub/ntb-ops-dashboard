# -*- coding: utf-8 -*-
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

app_path = r"c:\Users\lap4all\Desktop\New folder\templates\index.html"

with open(app_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Total lines in index.html:", len(lines))

query = "sendTelegram"
matches = []
for idx, line in enumerate(lines):
    if query in line:
        matches.append((idx + 1, line.strip()))
for m in matches:
    print(f"Line {m[0]}: {m[1]}")








# End of script


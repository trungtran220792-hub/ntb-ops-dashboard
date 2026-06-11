# -*- coding: utf-8 -*-
import os
import json

steps_dir = r"c:\Users\lap4all\Desktop\New folder\scratch\extracted_steps"
files = sorted(os.listdir(steps_dir))

for filename in files:
    filepath = os.path.join(steps_dir, filename)
    size = os.path.getsize(filepath)
    print(f"File: {filename} ({size} bytes)")
    with open(filepath, 'r', encoding='utf-8') as f:
        first_few_lines = [f.readline().strip() for _ in range(5)]
    print("  First few lines:")
    for line in first_few_lines:
        print(f"    {line}")

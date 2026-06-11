# -*- coding: utf-8 -*-
import os

scratch_dir = r"c:\Users\lap4all\Desktop\New folder\scratch"

for i in range(9):
    path = os.path.join(scratch_dir, f"recovered_table_func_{i}.js")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check if content contains truncation marker
        has_truncated = "truncated" in content or "..." in content
        print(f"File recovered_table_func_{i}.js: size={len(content)} chars, has_truncated={has_truncated}")
        
        # Let's write a clean version without any headers
        # Print the first 20 lines to see what is inside
        lines = content.splitlines()
        print(f"  First 5 lines: {lines[:5]}")
        print(f"  Last 5 lines: {lines[-5:]}")
        print("-" * 50)

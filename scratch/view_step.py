# -*- coding: utf-8 -*-
import os

transcript_path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\2742477c-f9ad-4ec9-923d-4fdf4f5c14ba\.system_generated\logs\transcript.jsonl"
out_path = r"c:\Users\lap4all\Desktop\New folder\scratch\step_2910_raw.txt"

if os.path.exists(transcript_path):
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            if '"step_index":2910' in line or '"step_index": 2910' in line:
                with open(out_path, 'w', encoding='utf-8') as out:
                    out.write(line)
                print("Saved step 2910 raw to step_2910_raw.txt")
                break
else:
    print("Transcript not found")

# -*- coding: utf-8 -*-
import codecs

paths = {
    "current": r"c:\Users\lap4all\Desktop\New folder\templates\index.html",
    "backup": r"c:\Users\lap4all\Desktop\New folder\scratch\templates\index.html"
}
outpath = r"c:\Users\lap4all\Desktop\New folder\scratch\search_results.txt"

terms = ['escapeHTML', 'function escapeHTML']

with codecs.open(outpath, 'w', 'utf-8') as out:
    for name, filepath in paths.items():
        out.write(f"=== File: {name} ({filepath}) ===\n")
        try:
            with codecs.open(filepath, 'r', 'utf-8') as f:
                lines = f.readlines()
            for i, line in enumerate(lines):
                for term in terms:
                    if term in line:
                        out.write(f"Line {i+1}: {line.strip()[:150]}\n")
                        break
        except Exception as e:
            out.write(f"Error reading {name}: {str(e)}\n")

print("Done scanning. Saved results to scratch/search_results.txt")



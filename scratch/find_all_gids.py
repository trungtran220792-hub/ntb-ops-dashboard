import urllib.request
import re

url = "https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit"
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    
    # GIDs are typically 8-10 digit numbers, or 0.
    # Let's search for numbers of length 8-10.
    numbers = re.findall(r'\b\d{8,10}\b', html)
    print("Numbers found:", len(numbers))
    unique_numbers = set(numbers)
    print("Unique numbers:", len(unique_numbers))
    
    # Let's see if we can find them in the context of JSON or JavaScript arrays
    # E.g., looking for sheetId, gridId, etc.
    out = []
    for num in unique_numbers:
        pos = 0
        while True:
            pos = html.find(num, pos)
            if pos == -1:
                break
            snippet = html[max(0, pos-50):min(len(html), pos+50)]
            snippet = " ".join(snippet.split())
            out.append(f"Number {num} at {pos}: {snippet}")
            pos += len(num)
            
    with open("scratch/gids_context.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("Done writing scratch/gids_context.txt")
    
except Exception as e:
    print("Error:", e)

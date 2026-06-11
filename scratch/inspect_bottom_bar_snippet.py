import urllib.request

url = "https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit"
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    
    pos = html.find('id="grid-bottom-bar"')
    if pos != -1:
        snippet = html[pos:pos+4000]
        with open("scratch/bottom_bar_snippet.txt", "w", encoding="utf-8") as f:
            f.write(snippet)
        print("Done writing snippet. Length:", len(snippet))
    else:
        print("grid-bottom-bar not found in HTML!")
except Exception as e:
    print("Error:", e)

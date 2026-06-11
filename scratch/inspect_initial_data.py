import urllib.request

url = "https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit"
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    
    found = False
    for line in html.splitlines():
        if "_W_initialData" in line or "bootstrapData" in line or "_bootstrap" in line:
            with open("scratch/initial_data_line.txt", "w", encoding="utf-8") as f:
                f.write(line)
            print("Done writing initial_data_line.txt. Length:", len(line))
            found = True
            break
    if not found:
        print("No match found for bootstrap or initial data line!")
except Exception as e:
    print("Error:", e)

import urllib.request
import re

url = "https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit"
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    
    # Let's try to match:
    # [0,0,\"352488066\",[{\"1\":[[0,0,\"OPR\"
    # Wait, the double quotes around numbers and strings inside the JSON string are escaped.
    # The JSON string itself is in a list, like:
    # [21350203,"[0,0,\"352488066\",[{\"1\":[[0,0,\"OPR\"
    # Let's match:
    # \[\s*0\s*,\s*0\s*,\s*\\"?(\d+)\\"?\s*,\s*\[\s*\{\s*\\"?1\\"?\s*:\s*\[\s*\[\s*0\s*,\s*0\s*,\s*\\"?([^\\"]+)\\"?
    pattern = r'\[\s*\d+\s*,\s*0\s*,\s*\\"?(\d+)\\"?\s*,\s*\[\s*\{\s*\\"?1\\"?\s*:\s*\[\s*\[\s*0\s*,\s*0\s*,\s*\\"?([^\\"\(\]]+)\\"?'
    matches = re.findall(pattern, html)
    print("Matches found:", len(matches))
    for gid, name in matches:
        print(f"  {name} -> {gid}")
        
except Exception as e:
    print("Error:", e)

# -*- coding: utf-8 -*-
import os

p = r"c:\Users\lap4all\Desktop\New folder\scratch\index.html.base"
if os.path.exists(p):
    with open(p, 'rb') as f:
        data = f.read(100)
    print("Bytes:", data)
    print("Hex:", data.hex())
else:
    print("File not found")

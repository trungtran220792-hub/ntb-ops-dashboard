# -*- coding: utf-8 -*-
from html.parser import HTMLParser
import sys

class SimpleHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
        
    def handle_error(self, message):
        self.errors.append(message)

def verify_html():
    sys.stdout.reconfigure(encoding='utf-8')
    path = "templates/index.html"
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        parser = SimpleHTMLParser()
        parser.feed(content)
        if parser.errors:
            print("HTML parsing errors found:")
            for err in parser.errors:
                print(" ", err)
        else:
            print("HTML structure parsed with no syntax errors!")
    except Exception as e:
        print("Error verifying HTML:", e)

if __name__ == "__main__":
    verify_html()

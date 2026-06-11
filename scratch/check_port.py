import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind(('127.0.0.1', 5000))
    s.close()
    print("Port 5000 is FREE")
except socket.error:
    print("Port 5000 is IN USE")

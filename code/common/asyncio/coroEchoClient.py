#!/usr/bin/python
import socket
import sys
import time

t = int(sys.argv[1])

clisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clisock.connect(('127.0.0.1', 8888))
print(f"sleep {t} sec")
time.sleep(t)
clisock.send(b"Hello World")
print(f"send after")
print(clisock.recv(100))
clisock.close()

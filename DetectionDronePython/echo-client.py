#!/usr/bin/env python3

import socket

HOST = "192.168.1.240"  # The server's hostname or IP address
PORT = 8080  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall("Hello, world")
    data = s.recv(1024)

print("Received", repr(data))

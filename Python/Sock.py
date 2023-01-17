"""
{ send coordinates to unity }

the function will be written after adding asynchrony
"""
import socket

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()

print('connected:', addr)
print(sock)
print(sock.bind)

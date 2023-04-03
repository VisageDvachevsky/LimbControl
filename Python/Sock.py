"""
{ send coordinates to unity }

"""
import socket

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()

print('connected:', addr)
print(sock)
print(sock.bind)

import socket
def one():
	sock = socket.socket()
	sock.connect(('localhost', 9090))
def two():
	sock = socket.socket()
	sock.connect(('localhost', 9090))

one()
two()
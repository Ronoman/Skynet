import socket

sock = sock.bind(("", 1001))

with open("output.csv") as out:
	while True:
		message, address = sock.recvfrom(1024)
		out.write(message.decode("utf-8"))
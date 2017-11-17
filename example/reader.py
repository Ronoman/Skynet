import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 1001))

with open("output.csv", "w+") as out:
	while True:
		print("listening")
		message, address = sock.recvfrom(1024)
		out.write(message.decode("utf-8") + "\n")
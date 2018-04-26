import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 1001))

while True:
    # i += 1
    message, address = sock.recvfrom(1024)
    message = message.decode("utf-8")

    print(message)

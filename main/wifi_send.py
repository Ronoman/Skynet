import socket
import time
import joystick
UDP_IP = "10.76.0.100" #Change depending on the network (TODO: read from file)
UDP_PORT = 1001

joy = None

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((UDP_IP, UDP_PORT))

joy = joystick.getFirstJoystick()
print(type(joy))

@joy.event
def on_axis(axis, value):
    print("axis: " +str(axis) + ", val: " + str(value))
    if(axis == "l_thumb_y" or axis == "r_thumb_x"):
        sock.sendto(axis + "," + str(value), (UDP_IP, UDP_PORT))

print("starting loop")
while True:
    joy.dispatch_events()
    time.sleep(0.01)

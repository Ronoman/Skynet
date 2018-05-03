import socket
import time
import joystick
UDP_IP = "192.168.43.100" #Change depending on the network (TODO: read from file)
UDP_PORT = 1001

joy = None

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

joy = joystick.getFirstJoystick()
print(type(joy))

@joy.event
def on_axis(axis, value):
    print("axis: " +str(axis) + ", val: " + str((value*2)**2))
    if(axis == "l_thumb_y" or axis == "r_thumb_x"):
        sock.sendto(axis + "," + str((value*2)**2), (UDP_IP, UDP_PORT))

@joy.event
def on_button(button, pressed):
    print("button: " + str(button) + ", pressed: " + str(pressed))
    if(str(button) == "13"):
        sock.sendto("kill")

print("starting loop")
while True:
    joy.dispatch_events()
    time.sleep(0.01)

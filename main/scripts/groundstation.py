from matplotlib import pyplot as plt
from threading import Thread
import joystick
import socket
import time
import math

REMOTE_IP = "192.168.43.100" #Change depending on the network (currently Eli's hotspot)
REMOTE_PORT = 1001

joy = None

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 1001)) #For receiving gyro data

joy = joystick.getFirstJoystick()

#All matplotlib plotting
def gyroReceiver():
    message, address = sock.recvfrom(128)
    message = message.decode("utf-8")
    message = message.split(',')
    message = [float(x) for x in message]

    ts = [message[0]]
    x = [message[1]]
    y = [message[2]]
    z = [message[3]]

    first = True

    dxPlot, = plt.plot(ts, x)
    dyPlot, = plt.plot(ts, y)
    dzPlot, = plt.plot(ts, z)

    plt.ion()
    plt.show()
    axes = plt.gca()
    axes.set_ylim([-90,90])

    # i=0
    i = message[0]
    start = time.time()
    while True:
        # i += 1
        message, address = sock.recvfrom(1024)
        message = message.decode("utf-8")
        message = message.split(',')

        message = [float(x) for x in message]

        ts = ts + [message[0]]
        x = x + [message[1]]
        y = y + [message[2]]
        z = z + [message[3]]

        first = False
        ts = ts[-100:]
        x = x[-100:]
        y = y[-100:]
        z = z[-100:]

        dxPlot.set_xdata(ts)
        dyPlot.set_xdata(ts)
        dzPlot.set_xdata(ts)

        dxPlot.set_ydata(x)
        dyPlot.set_ydata(y)
        dzPlot.set_ydata(z)

        dxPlot.set_label(str(x[-1]))
        dyPlot.set_label(str(y[-1]))
        dzPlot.set_label(str(z[-1]))

        axes.set_xlim([ts[0],message[0]])
        plt.draw()
        plt.pause(0.0001)
        #print("dt: " + str(ts[-1]) + "\t\tx: " + str(x[-1]) + "\t\ty: " + str(y[-1]) + "\t\tz: " + str(z[-1]))

#Joystick updater
def joystickUpdater():
    joy.dispatch_events()
    time.sleep(0.05)

@joy.event
def on_axis(axis, value):
    print("axis: " +str(axis) + ", val: " + str((value*2)**2))
    if(axis == "l_thumb_y" or axis == "r_thumb_x" or axis == "r_thumb_y"):
        sock.sendto(axis + "," + str((value*2)**2*(value/abs(value))), (REMOTE_IP, REMOTE_PORT))

@joy.event
def on_button(button, pressed):
    print("button: " + str(button) + ", pressed: " + str(pressed))
    if(str(button) == "13"):
        sock.sendto("kill", (REMOTE_IP, REMOTE_PORT))

if __name__ == "__main__":
    updaterThread = Thread(target=joystickUpdater, args=())
    updaterThread.daemon = True

    receiverThread = Thread(target=gyroReceiver, args=())
    receiverThread.daemon = True

    updateThread.start()
    receiverThread.start()

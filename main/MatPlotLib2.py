import math
from matplotlib import pyplot as plt

import numpy as np
import time
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 1001))

message, address = sock.recvfrom(64)
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
axes.set_ylim([-360,360])

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
    #x = x + [message[1]]
    #y = y + [message[2]]
    z = z + [message[3]]

    first = False
    ts = ts[-100:]
    #x = x[-100:]
    #y = y[-100:]
    z = z[-100:]

    dxPlot.set_xdata(ts)
    #dyPlot.set_xdata(ts)
    #dzPlot.set_xdata(ts)

    #dxPlot.set_ydata(x)
    #dyPlot.set_ydata(y)
    dzPlot.set_ydata(z)

    axes.set_xlim([ts[0],message[0]])

    plt.draw()
    plt.pause(0.0001)

finish = time.time()
print("Data Time Elapsed: ",(message[0]-i)/1000, "seconds")
print("Actual Time Elapsed: ",finish-start, " seconds")

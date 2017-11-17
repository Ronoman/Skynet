#Trying Shit out
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

x = [message[0]]
dx = [message[1]]
dy = [message[2]]
dz = [message[3]]

px = [0]
py = [0]
pz = [0]
#=E2+(B2*(A3-A2)/1000)
first = True

dxPlot, = plt.plot(x, dx)
dyPlot, = plt.plot(x, dy)
dzPlot, = plt.plot(x, dz)

plt.ion()
plt.show()
axes = plt.gca()
axes.set_ylim([-360,360])

# i=0
i = message[0]
start = time.time()
while True:
    # i += 1
    message, address = sock.recvfrom(64)
    message = message.decode("utf-8")
    message = message.split(',')

    message = [float(x) for x in message]

    x = x + [message[0]]
    dx = dx + [message[1]]
    dy = dy + [message[2]]
    dz = dz + [message[3]]
    
    if not first:
        px.append(px[-1] + (dx[-1]*(x[-1]-x[-2])/1000))
        py.append(py[-1] + (dy[-1]*(x[-1]-x[-2])/1000))
        pz.append(pz[-1] + (dz[-1]*(x[-1]-x[-2])/1000))
    else:
        px.append(0)
        py.append(0)
        pz.append(0)
        
    first = False
    x = x[-100:]
    dx = dx[-100:]
    dy = dy[-100:]
    dz = dz[-100:]
    
    px = px[-100:]
    py = py[-100:]
    pz = pz[-100:]

    dxPlot.set_xdata(x)
    dyPlot.set_xdata(x)
    dzPlot.set_xdata(x)

    dxPlot.set_ydata(dx)
    dyPlot.set_ydata(dy)
    dzPlot.set_ydata(dz)

    axes.set_xlim([x[0],message[0]])

    plt.draw()
    plt.pause(0.0001)

finish = time.time()
print("Data Time Elapsed: ",(message[0]-i)/1000, "seconds")
print("Actual Time Elapsed: ",finish-start, " seconds")

#Trying Shit out
import math
from matplotlib import pyplot as plt

import numpy as np
import time
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 1001))

message, address = sock.recvfrom(1024)
message = message.decode("utf-8")
message = message.split(',')
message = [float(x) for x in message]

x = [message[0]]
y1 = [message[1]]
y2 = [message[2]]
y3 = [message[3]]

y1Plot, = plt.plot(x, y1)
y2Plot, = plt.plot(x, y2)
y3Plot, = plt.plot(x, y3)

plt.ion()
plt.show()
axes = plt.gca()
axes.set_ylim([-300,300])

# i=0
i = message[0]
start = time.time()
while (message[0]-i)<10000:
    # i += 1
    message, address = sock.recvfrom(1024)
    message = message.decode("utf-8")
    message = message.split(',')

    message = [float(x) for x in message]

    # print("datapoint: ",(message[0]-i)/1000)

    x = np.append(x, message[0])
    y1 = np.append(y1, message[1])
    y2 = np.append(y2, message[2])
    y3 = np.append(y3, message[3])

    y1Plot.set_xdata(x)
    y2Plot.set_xdata(x)
    y3Plot.set_xdata(x)

    y1Plot.set_ydata(y1)
    y2Plot.set_ydata(y2)
    y3Plot.set_ydata(y3)

    axes.set_xlim([x[0],message[0]])

    plt.draw()
    plt.pause(0.001)

finish = time.time()
print("Data Time Elapsed: ",(message[0]-i)/1000, "seconds")
print("Actual Time Elapsed: ",finish-start, " seconds")

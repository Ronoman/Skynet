#Testing PID Class
import pid
from random import randrange
import matplotlib.pyplot as plt

#initializes data to graph
data = 0.0
print("setpoint:", data)
x = [0]
y = [data]
sety = [0, 0]

#sets up PID
myPid = pid.PID(0.0, .5, 0, 0)

#introduces error
data = float(randrange(-100, 100))
#data = 50
print("error:", data)
x.append(1)
y.append(data)

"""#fixes error
i = 2
while abs(data - myPid.setpoint) > .001:
    data = data - myPid.update(data)
    x.append(i)
    i += 1
    y.append(data)
    sety.append(0)
    print(data)"""

#fixes error
i = 2
while abs(data - myPid.setpoint) > .001:
    if i % 2 == 0:
        data = data - myPid.update(data) + randrange(-10, 10)/randrange(75, 100)
    else:
        data = data - myPid.update(data)
    if i == 75:
        data = data + randrange(-50, 50)
    x.append(i)
    i += 1
    y.append(data)
    sety.append(0)
    print(data)

#plots data
plt.plot(x, sety, color = "gray", linestyle = "--")
plt.plot(x, y, "r")
plt.xlabel("Cycle")
plt.ylabel("Error")
plt.title("Error Correction to Setpoint")
plt.show()

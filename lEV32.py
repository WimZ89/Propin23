'''
Created on Sep 2, 2020
Proof that it is impossible to make a force without a counteforce
@author: wimz
'''

import numpy as np

from math import pi
from numpy import arange,sin,cos
import matplotlib.pyplot as plt

# from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLabel, QHBoxLayout, QSizePolicy)
import matplotlib.animation as animation



def update_line(num, data, line):
    line.set_data(data[..., :num])
    return line,

fig1 = plt.figure()




f=1.0       # frequency
t=0.0       # current time
tstep=0.02  #time step
r=1.0       #radius
tstep *= 10

def close(a,b,error):
    if a > b + error*a:
        return False
    if a < b - error*a:
        return False
    return True

assert (    close(1,1.01,0.015))
assert (not close(1,1.01,0.005))
assert (    close(1,0.99,0.015))
assert (not close(1,0.99,0.005))

def angle(ti,centerangle,sweepangle, frequency):
    p=[centerangle + sweepangle * sin(t*frequency) for t in ti]
    return p 

print (angle([1],1,2,1))
print (1+2*sin(1*1))
# exit(0)
assert ( close( angle([0],1,2,1)[0], 1.0, 0.0001))
assert ( close( angle([1],1,2,1)[0],1+2*sin(1*1),0.0001))


centerangle,sweepangle = pi/4.0,pi/8.0

time=arange(-pi/2 , pi/2+tstep, tstep )
ang=angle(time,centerangle,sweepangle, f)

assert ( close( np.max(ang), centerangle + sweepangle, 0.01))
assert ( close( np.min(ang), centerangle - sweepangle, 0.01))

assert (2==2)
# assert (max(ang)=)

x = [ r*sin(a) for a in ang] 
y = [ r*cos(a) for a in ang] 

positions =np.array([x,y]) # position at given time


# speed depends on previous position and time it took to go there 
Speed = np.diff(positions)/tstep   
print (Speed)
# speed depends on previous speed and time it took to change it 
Accel = np.diff(Speed)/tstep
print (Accel)

exit(0)



l, = plt.plot([], [], 'r-')

plotdata=positions

plt.xlim(np.amin(plotdata[0]),np.amax(plotdata[0]))
plt.ylim(np.amin(plotdata[1]),np.amax(plotdata[1]))

plt.xlabel('x')
plt.title('test')
line_ani = animation.FuncAnimation(fig1, update_line, len(time), fargs=(plotdata, l),
                                    interval=50, blit=True)
# plt.scatter(x,y)
plt.show()



print ("Done" , len(time))


# def difff(xy):
#     x,y=[],[]
#     print("len",len(xy[0]))
#     for i in range(len(xy[0])-1):
#         print (i)
#         x.append(xy[0][i+1]-xy[0][i])
#         y.append(xy[1][i+1]-xy[1][i])
#     return np.array([x,y])
# data = difff(data) np. does exactly the same.

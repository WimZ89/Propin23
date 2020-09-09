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

# Fixing random state for reproducibility
# np.random.seed(19680801)


# To save the animation, use the command: line_ani.save('lines.mp4')


f=1.0 # frequency
t=0.0 # current time
tstep=0.02 #time step
r=1.0   #radius



def angle(ti):
    p=[pi/4.0 + pi/4.0 * sin(t*f) for t in ti]
    return p 

def difff(xy):
    x,y=[],[]
    print("len",len(xy[0]))
    for i in range(len(xy[0])-1):
        print (i)
        x.append(xy[0][i+1]-xy[0][i])
        y.append(xy[1][i+1]-xy[1][i])
    return np.array([x,y])


time=arange(-pi/2 , pi/2+tstep, tstep )
ang=angle(time)

# ang=arange(0, pi/4+tstep, tstep )

x = [ r*sin(a) for a in ang] 
y = [ r*cos(a) for a in ang] 

# data = np.random.rand(2, 25)
# print (data)
# print()
# print (x)
# print (y)
# data = np.concatenate((x,y), axis=1)
data =np.array([x,y])
print (data)
# l, = plt.plot([], [], 'r-')


# 
# data = difff(data)
data = np.diff(data)/tstep
data = np.diff(data)/tstep
l, = plt.plot([], [], 'r-')
# plt.xlim(-1, 1)
# plt.ylim(0, 1)

plt.xlim(np.amin(data[0]),np.amax(data[0]))
plt.ylim(np.amin(data[1]),np.amax(data[1]))

plt.xlabel('x')
plt.title('test')
line_ani = animation.FuncAnimation(fig1, update_line, len(time), fargs=(data, l),
                                    interval=50, blit=True)
# plt.scatter(x,y)
plt.show()



print ("Done" , len(time))